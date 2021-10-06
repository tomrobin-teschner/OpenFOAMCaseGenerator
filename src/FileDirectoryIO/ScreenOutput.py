from src.Properties import GlobalVariables as Parameters


class ScreenOutput:
    def __init__(self, properties):
        self.properties = properties


    def print_summary(self, command_line_arguments):
        print('Application: OpenFOAMCaseGenerator')
        print('Copyright  : Tom-Robin Teschner, Cranfield University')
        print('License    : MIT')
        print('Version    : 2.0.0-alpha.10\n')

        if command_line_arguments.option_exists('input'):
            print('Using input    : input/' + command_line_arguments['input'] + '.py')
        else:
            print('Using input    : input/default.py')
        print('Generated case : ' + self.properties['file_properties']['path'])
        print('Reynolds number: ' + str(self.properties['flow_properties']['non_dimensional_properties']['Re']))

        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            print('Mach number    : ' + str(self.properties['flow_properties']['non_dimensional_properties']['Ma']))

        if self.properties['file_properties']['mesh_treatment'] == Parameters.NO_MESH:
            print('\nNo mesh was specified during the generation of case directory.'
                  '\nEnsure you copy a mesh manually before running your case')


