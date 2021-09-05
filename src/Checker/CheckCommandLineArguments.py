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
        --input=name                select a input file to use instead of the properties set in the code
        --output=name               output a json script along with the case setup as specified by the properties dictionary
        --write-json-only=name      output the case to a json file only, don't write the case setup
        '''
        for i in range(1, len(self.__args)):
            if '--input=' in self.__args[i]:
                self.__options['input'] = self.__args[i].replace('--input=', '')
            elif '--output=' in self.__args[i]:
                self.__options['output'] = self.__args[i].replace('--output=', '')
            elif '--write-json-only=' in self.__args[i]:
                self.__options['write-json-only'] = self.__args[i].replace('--write-json-only=', '')
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
