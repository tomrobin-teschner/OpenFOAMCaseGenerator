from src.Properties import GlobalVariables as Parameters


class ScreenOutput:
    def __init__(self, properties):
        self.properties = properties

    def print_summary(self, command_line_arguments):
        print('Application: OpenFOAMCaseGenerator')
        print('Copyright  : Tom-Robin Teschner, 2020-2021')
        print('License    : MIT')
        print('Version    : 2.0.0-alpha.13\n')

        if command_line_arguments.option_exists('input'):
            print('Using input    : input/' + command_line_arguments['input'] + '.py')
        else:
            print('Using input    : input/default.py')
        print('Generated case : ' + self.properties['file_properties']['path'])
        reynolds = self.properties['flow_properties']['non_dimensional_properties']['Re']
        if reynolds > 1:
            print('Reynolds number: ' + f'{reynolds:.0f}')
        else:
            print('Reynolds number: ' + f'{reynolds:8.2e}')

        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            mach = self.properties['flow_properties']['non_dimensional_properties']['Ma']
            if mach < 0.1:
                print('Mach number    : ' + f'{mach:8.2e}')
            else:
                print('Mach number    : ' + f'{mach:5.3f}')

        if self.properties['file_properties']['mesh_treatment'] == Parameters.NO_MESH:
            print('\nNo mesh was specified during the generation of case directory.'
                  '\nEnsure you copy a mesh manually before running your case')
