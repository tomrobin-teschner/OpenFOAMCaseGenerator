import subprocess
import os
import shutil


number_of_tests = 4


def test_all():
    test_path = os.path.join('tests', 'cases')
    create_test_directory(test_path)
    current_test_number = 1

    # run all tests here
    current_test_number = test_naca_0012(test_path, current_test_number)
    current_test_number = test_taylor_green_vortex(test_path, current_test_number)
    current_test_number = test_wing_and_winglet(test_path, current_test_number)

    # clean up after ourselves
    tear_down_test_directory(test_path)


def create_test_directory(test_path):
    if not os.path.exists(test_path):
        print('Generating temporary directory for testing at:', test_path, '\n')
        os.makedirs(test_path)


def tear_down_test_directory(test_path):
    print('\nDeleting testing directory at:', test_path)
    shutil.rmtree(test_path)


def test_naca_0012(test_path, current_test_number):
    run_directory = '--replace=file_properties/run_directory:' + test_path

    print('\033[94m[' + str(current_test_number) + '/' + str(number_of_tests) + ']\033[0m ', end='')
    print('Testing --input=naca_0012 ........................................................................ ', end='')
    base_test = ['python', 'OpenFOAMCaseGenerator.py', '--input=naca_0012', run_directory]
    subprocess.run(base_test, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('\033[92mDONE\033[0m')
    current_test_number += 1

    print('\033[94m[' + str(current_test_number) + '/' + str(number_of_tests) + ']\033[0m ', end='')
    print('Testing --input=naca_0012 --replace=flow_properties/flow_type:0 .................................. ', end='')
    modified_test_1 = base_test + ['--replace=flow_properties/flow_type:0']
    subprocess.run(modified_test_1, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('\033[92mDONE\033[0m')
    current_test_number += 1

    return current_test_number


def test_taylor_green_vortex(test_path, current_test_number):
    run_directory = '--replace=file_properties/run_directory:' + test_path

    print('\033[94m[' + str(current_test_number) + '/' + str(number_of_tests) + ']\033[0m ', end='')
    print('Testing --input=taylor_green_vortex .............................................................. ', end='')
    base_test = ['python', 'OpenFOAMCaseGenerator.py', '--input=taylor_green_vortex', run_directory]
    subprocess.run(base_test, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('\033[92mDONE\033[0m')
    current_test_number += 1

    return current_test_number


def test_wing_and_winglet(test_path, current_test_number):
    run_directory = '--replace=file_properties/run_directory:' + test_path

    print('\033[94m[' + str(current_test_number) + '/' + str(number_of_tests) + ']\033[0m ', end='')
    print('Testing --input=wing_and_winglet ................................................................. ', end='')
    base_test = ['python', 'OpenFOAMCaseGenerator.py', '--input=wing_and_winglet', run_directory]
    subprocess.run(base_test, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('\033[92mDONE\033[0m')
    current_test_number += 1

    return current_test_number


if __name__ == '__main__':
    test_all()
