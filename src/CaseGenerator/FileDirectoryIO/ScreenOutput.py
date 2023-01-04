import datetime
import fileinput
from src.CaseGenerator.Properties import GlobalVariables as Parameters

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
        print(f'Application     : OpenFOAMCaseGenerator')
        print(f'Source          : https://github.com/tomrobin-teschner/OpenFOAMCaseGenerator')
        print(f'Copyright       : Tom-Robin Teschner, {self.copyright}')
        print(f'License         : MIT')
        print(f'Version         : {self.version}\n')

        if command_line_arguments.option_exists('input'):
            print(f'Using input     : input/{command_line_arguments["input"]}.py')
        else:
            print('Using input     : input/default.py')
        print('Generated case  : ' + self.properties['file_properties']['path'])
        reynolds = self.properties['flow_properties']['non_dimensional_properties']['Re']
        if reynolds > 1:
            print('Reynolds number : ' + f'{reynolds:.0f}')
        else:
            print('Reynolds number : ' + f'{reynolds:8.2e}')

        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            mach = self.properties['flow_properties']['non_dimensional_properties']['Ma']
            if mach < 0.1:
                print('Mach number     : ' + f'{mach:8.2e}')
            else:
                print('Mach number     : ' + f'{mach:5.3f}')

        if self.properties['file_properties']['mesh_treatment'] == Parameters.NO_MESH:
            print('\nNo mesh was specified during the generation of case directory.'
                  '\nEnsure you copy a mesh manually before running your case')
