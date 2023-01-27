from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator import CaseGenerator
from src.CaseGenerator.Properties.CaseProperties import CaseProperties
from src.CaseGenerator.Properties.CaseFactory import CaseFactory

from os import path, listdir, makedirs
from sys import argv
from shutil import rmtree
import subprocess
import time
import importlib
import datetime

# directory into which temporary test files will be written
test_directory_name = path.join('tests', 'system', 'temp_test_cases')

# openfoam versions to test (will need to be installed)
of_versions = ['2006', '2012', '2106', '2112', '2206', '2212']

# openfoam root directory
of_root = path.join('usr', 'lib', 'openfoam')

class SystemTestManager():
    def __init__(self):
        self.tests = []
        self.total_tests = 0
        self.successful_test = 0
        self.test_failed = False

        filename = path.join(test_directory_name,'.gitignore')
        makedirs(path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write('*')

    def __del__(self):
        # clean up after ourselves, but only if tests didn't fail (so output can be inspected)
        if not self.test_failed:
            if path.exists(test_directory_name):
                rmtree(test_directory_name)

    def find_all_tests(self):
        for dir in listdir(path.join('tests', 'system')):
            if (
                    path.isdir(path.join('tests', 'system', dir)) and
                    dir != path.basename(path.normpath(test_directory_name)) and
                    dir != '__pycache__'
                ):
                test_case = getattr(importlib.import_module(f'tests.system.{dir}.{dir}'), dir)
                test = test_case()
                for parameters in test.setup_case():
                    self.__register_case(parameters[0], parameters[1], parameters[2])

    def __register_case(self, module, case_name, parameters):
        factory         = CaseFactory(module, parameters)
        case_properties = factory.get_case_properties()

        # overwrite properties for testing
        case_properties = self.__overwrite_test_specific_settings(case_properties, case_name)

        case = CaseGenerator(case_properties, True)
        case.generate_case()
        self.tests.append(case_name)

    def run_all_tests(self):
        if (len(self.tests) > 0):
            versions_to_use = []
            if '--latestVersionOnly' in argv:
                versions_to_use.append(of_versions[-1])
            else:
                versions_to_use = of_versions
            
            self.__print_pre_test_statistics(versions_to_use)
            max_case_length = self.__get_max_length_of_case_name()
            self.__print_header(max_case_length, versions_to_use)
            
            start_time = time.time()
            self.__run_all_tests(max_case_length, versions_to_use)
            end_time = time.time()

            self.__print_footer(max_case_length, versions_to_use)
            self.__print_post_test_statistics(start_time, end_time)

    def __overwrite_test_specific_settings(self, case_properties, case_name):
        case_handler    = CaseProperties()

        test_path = test_directory_name
        case_properties['file_properties']['run_directory'] = test_path
        case_properties['file_properties']['case_name'] = case_name
        case_properties = case_handler.add_default_properties(case_properties)

        # run all test on single core
        case_properties['parallel_properties']['run_in_parallel'] = False

        time_integration = case_properties['time_discretisation']['time_integration']
        if time_integration == TimeTreatment.steady_state:
            case_properties['time_discretisation']['steady_state_properties']['startTime'] = 0
            case_properties['time_discretisation']['steady_state_properties']['endTime'] = 1
            case_properties['time_discretisation']['steady_state_properties']['deltaT'] = 1
            case_properties['time_discretisation']['steady_state_properties']['CFLBasedTimeStepping'] = False
        elif time_integration == TimeTreatment.unsteady:
            case_properties['time_discretisation']['unsteady_properties']['startTime'] = 0
            case_properties['time_discretisation']['unsteady_properties']['endTime'] = 1e-10
            case_properties['time_discretisation']['unsteady_properties']['deltaT'] = 1e-10
            case_properties['time_discretisation']['unsteady_properties']['CFLBasedTimeStepping'] = False
        return case_properties

    def __get_max_length_of_case_name(self):
        length = 0
        for case in self.tests:
            if len(case) > length:
                length = len(case)
        return length

    def __print_header(self, max_case_length, versions):
        padding = '-'*max_case_length
        print(f'Case{padding}|', end='')
        for version in versions:
            print(f'-v{version}-|', end='')
        print('')

    def __print_footer(self, max_case_length, versions):
        padding = '-'*max_case_length
        print(f'----{padding}|', end='')
        for version in versions:
            print(f'-------|', end='')
        print('')

    def __run_test(self, test, version):
        test_command = (
                        f'bash -c "source /usr/lib/openfoam/openfoam{version}/etc/bashrc && '
                        f'cd {path.join(test_directory_name, test)} && '
                        f'./Allrun"'
                    )
        out = subprocess.run(test_command, shell=True, capture_output=True, text=True)
        self.total_tests += 1
        return out

    def __check_test(self, test, version, out):
        stdout = out.stdout
        stderr = out.stderr

        if 'FOAM FATAL ERROR' in stdout or 'FOAM FATAL ERROR' in stderr:
            self.__test_fail(test, version, stdout, stderr)
        elif 'FOAM FATAL IO ERROR' in stdout or 'FOAM FATAL IO ERROR' in stderr:
            self.__test_fail(test, version, stdout, stderr)
        elif 'not found in dictionary' in stdout or 'not found in dictionary' in stderr:
            self.__test_fail(test, version, stdout, stderr)
        elif 'FOAM exiting' in stdout or 'FOAM exiting' in stderr:
            self.__test_fail(test, version, stdout, stderr)
        elif 'Foam::error::printStack' in stdout or 'Foam::error::printStack' in stderr:
            self.__test_fail(test, version, stdout, stderr)
        elif 'End\n' in stdout:
            self.__test_pass()
        else:
            self.__test_fail(test, version, stdout, stderr)
            print(f'\n\nUncaught error, see log dump below. Exiting system tests')
            print('======================================================')
            print('======================= STDOUT =======================')
            print('======================================================')
            print(stdout)
            print('======================================================')
            print('======================= STDOUT =======================')
            print('======================================================')
            print(stderr)
            print('======================================================')
            print('======================= END ==========================')
            print('======================================================')
            exit(-1)

    def __run_all_tests(self, max_case_length, versions):
        for test in self.tests:
            print(f'{test:{max_case_length}}    |', end='', flush=True)
            for version in versions:
                out = self.__run_test(test, version)                    
                self.__check_test(test, version, out)
            print('', flush=True)
    
    def __print_pre_test_statistics(self, versions):
        print('Executing System Tests')
        print(f'Date: {datetime.date.today()}')
        print(f'Time: {datetime.datetime.now().strftime("%H:%M:%S")}\n')
        print(f'Number of test cases:                {len(self.tests)}')
        print(f'Number of OpenFOAM versions to test: {len(versions)}')
        print(f'Test matrix size:                    {len(self.tests) * len(versions)}\n')

    def __print_post_test_statistics(self, start_time, end_time):
        print('')
        if (self.total_tests > 0):
            successrate = int(100 * (self.successful_test / self.total_tests))
            print(f'\nSuccessful tests / total tests: {self.successful_test} / {self.total_tests} ({successrate}%)')
        print(f'Execution time                : {end_time - start_time:6.1f} seconds')

    def __test_pass(self):
        print(' \033[92mpass\033[0m  |', end='', flush=True)
        self.successful_test += 1

    def __test_fail(self, test, version, stdout, stderr):
        self.test_failed = True
        print(' \033[91mfail\033[0m  |', end='', flush=True)

        file_out = open(path.join(test_directory_name, f'{test}_{version}.stdout'), 'w')
        file_out.writelines(stdout)
        file_out.close()

        file_err = open(path.join(test_directory_name, f'{test}_{version}.stderr'), 'w')
        file_err.writelines(stderr)
        file_err.close()


if __name__ == '__main__':
    test_manager = SystemTestManager()
    test_manager.find_all_tests()
    test_manager.run_all_tests()
