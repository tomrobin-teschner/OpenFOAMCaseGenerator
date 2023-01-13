import datetime
import importlib
from src.CaseGenerator.Properties.GlobalVariables import *
from enum import Enum

# set current software version here. Will be printed to screen and automatically updated in README.md file
version_major = 2
version_minor = 1
version_patch = 1

class ScreenOutput:
    def __init__(self, properties):
        self.properties = properties
        self.copyright = f'2020-{datetime.date.today().year}'
        self.version = f'{version_major}.{version_minor}.{version_patch}'
        
        # overwrite version in README.md file
        file_id = open('README.md', 'r')
        all_lines = file_id.readlines()
        file_id.close()

        for index in range(0, len(all_lines)):
            if all_lines[index].find('https://img.shields.io/badge/Version-v') != -1:
                all_lines[index] = (
                    f'[![Generic badge]'
                    f'(https://img.shields.io/badge/Version-v{self.version}-red.svg)]'
                    f'(https://shields.io/)\n'
                )
        file_id = open('README.md', 'w')
        file_id.writelines(all_lines)
        file_id.close()

    def print_summary(self, command_line_arguments):
        print(f'Application    : OpenFOAMCaseGenerator')
        print(f'Source         : https://github.com/tomrobin-teschner/OpenFOAMCaseGenerator')
        print(f'Copyright      : Tom-Robin Teschner, {self.copyright}')
        print(f'License        : MIT')
        print(f'Version        : {self.version}\n')

        case = command_line_arguments['case']
        print(f'Generated case : {self.properties["file_properties"]["path"]}')
        print(f'Using input    : setups/cases/{case}/{case}.py\n')

        properties_module = command_line_arguments['case']
        case = getattr(importlib.import_module('setups.cases.'+properties_module+'.'+properties_module),
            properties_module)
        if command_line_arguments.get_number_of_parameters() + len(case.parameters) > 0:
            max_key_length = 0
            for key in case.parameters.keys():
                if len(key) > max_key_length:
                    max_key_length = len(key)
            max_key_length += 1

            print('Case parameters')
            for key, value in case.parameters.items():
                print(f'  - {key:{max_key_length}s}: {value}')

        if self.properties['file_properties']['mesh_treatment'] == Mesh.no_mesh:
            print('\nNo mesh was specified during the generation of case directory.'
                  '\nEnsure you copy a mesh manually before running your case')