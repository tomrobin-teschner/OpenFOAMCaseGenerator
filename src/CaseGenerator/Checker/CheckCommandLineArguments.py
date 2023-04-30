import sys
import os


class CheckCommandLineArguments:
    def __init__(self):
        self.__args = sys.argv
        self.__options = {}
        self.__process_command_line_arguments()

    def __process_command_line_arguments(self):
        help = \
        '''
        OpenFOAMCaseGenerator is a utility script that quickly produces a base case setup for OpenFOAM that alleviates
        the need to copy and modify tutorial cases. See the README.md file for more detailed information. To run all
        tests, simply run the test_all.py file within the test folder (requires python to be in your PATH) from the root
        folder.
        
        The syntax for running the actual case generator is
        
        python3 OpenFOAMCaseGenerator.py <options>
        
        A list of options is listed below
        
        --help                      prints this help menu

        --case=name                 (required) Specify here the name of the case setup to be processed. The case setup
                                    is expected in the input/ directory. Use the name of the folder (case sensitive).
                                    Note that there is a python file inside each case directory which implements a
                                    class. The case directory folder, the python name and the name of the class must all
                                    be the same, otherwise an error is thrown.

        --parameter:key=value       Sets the parameter with the name of key to a specific value. Parameters are
                                    case-specific and can be viewed either directly in the defining module (*.py file)
                                    or by running the case generator, if a case has parameters defined, these will be
                                    listed at the bottom.

        -p:key=value                Same as --parameter:key=value, short-hand notation

        --no-checks                 Run the case generator again but suppress any warnings and/or error messages

        --list-cases                List all available cases for which a valid setup exist
        '''

        self.__options['parameter'] = {}
        self.__options['no-checks'] = False
        for i in range(1, len(self.__args)):
            if '--case=' in self.__args[i]:
                self.__options['case'] = self.__args[i].replace('--case=', '')
            if '--no-checks' in self.__args[i]:
                self.__options['no-checks'] = True
            if '--parameter' in self.__args[i]:
                key_value = self.__args[i].replace('--parameter:', '').split('=')
                self.__options['parameter'][key_value[0]] = key_value[1]
            if '-p:' in self.__args[i]:
                key_value = self.__args[i].replace('-p:', '').split('=')
                self.__options['parameter'][key_value[0]] = key_value[1]
            if '--list-cases' in self.__args[i]:
                print('\nAvailable case setups:')
                for root, dirs, files in os.walk(os.path.join('input', 'cases'), topdown=True):
                    for dir in dirs:
                        if 'pycache' not in dir:
                            if 'BaseCase' not in dir:
                                print('- ', dir)
                exit(0)
            if '--help' in self.__args[i]:
                print(help)
                exit(0)


    def __getitem__(self, item):
        if item in self.__options:
            return self.__options[item]
        else:
            raise Exception(f'{item} not in command line arguments')

    def option_exists(self, option):
        if option in self.__options:
            return True
        else:
            return False

    def get_number_of_parameters(self):
        return len(self.__options['parameter'])

    def add_option(self, key, value):
        '''required for unit testing'''
        self.__options[key] = value
