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

        --replace=key:value         Replace a key value pair in the settings. This helps to change local parameters
                                    without having to change the actual module file, e.g. changing the angle of attack
                                    or Reynolds number as part of a parametric study. Ensure the key is provided with
                                    the full path to the parameter. For example, to change the Reynolds number, use
                                    --replace=flow_properties/non_dimensional_properties/Re:1000
                                    Note that properties are case sensitive. You can also use several replace statements
                                    to change more than one parameter. All changed parameters are appended to the case
                                    name, so with the above example, if we have the case name NACA, using the replace
                                    statement would change that to NACA_Re_1000.
        '''

        self.__options['replace'] = []
        for i in range(1, len(self.__args)):
            if '--input=' in self.__args[i]:
                self.__options['input'] = self.__args[i].replace('--input=', '')
            elif '--replace' in self.__args[i]:
                self.__options['replace'].append(self.__args[i].replace('--replace=', ''))
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
