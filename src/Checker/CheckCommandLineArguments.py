import sys


class CheckCommandLineArguments:
    def __init__(self):
        self.__args = sys.argv
        self.__options = {}
        self.__process_command_line_arguments()

    def __process_command_line_arguments(self):
        help = \
        '''
        OpenFOAMCaseGenerator is a utility script that quickly produces a base case setup for OpenFOAM that alleviates
        the need to copy and modify tutorial cases. See the README.md file for more detailed information.
        
        --help                      prints this help menu
        --input=name                specify the module to be used for input within the input/properties directory.
                                    specify file name here without ending, i.e. naca_0012, not naca_0012.py. if no input
                                    is specified, the default case properties will be processed, i.e.
                                    input/properties/default.py
        '''
        for i in range(1, len(self.__args)):
            if '--input=' in self.__args[i]:
                self.__options['input'] = self.__args[i].replace('--input=', '')
            elif '--help' in self.__args[i]:
                print(help)
                exit(0)
            else:
                raise Exception(help)

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
