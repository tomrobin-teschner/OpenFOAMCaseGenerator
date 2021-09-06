from input import GlobalVariables as Parameters


class ScreenOutput:
    def __init__(self, properties):
        self.properties = properties


    def print_summary(self):
        print('Running application OpenFOAMCaseGenerator')
        print('Copyright by Tom-Robin Teschner, Cranfield University\n')

        print('Generated case : ' + self.properties['file_properties']['path'])
        print('Reynolds number: ' + str(self.properties['flow_properties']['non_dimensional_properties']['Re']))

        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            print('Mach number    : ' + str(self.properties['flow_properties']['non_dimensional_properties']['Ma']))

        if self.properties['file_properties']['mesh_treatment'] == Parameters.NO_MESH:
            print('\nNo mesh was specified during the generation of case directory.'
                  '\nEnsure you copy a mesh manually before running your case')


