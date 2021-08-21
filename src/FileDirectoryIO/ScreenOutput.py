from src import GlobalVariables as Parameters


class ScreenOutput:
    def __init__(self, properties):
        self.properties = properties


    def print_summary(self):
        print('Running application OpenFOAMCaseGenerator')
        print('Copyright 2020 - 2021 by Tom-Robin Teschner, Cranfield University\n')

        print('Generated case : ' + self.properties['file_properties']['path'])
        print('Reynolds number: ' + str(self.properties['flow_properties']['reynolds_number']))
        if self.properties['file_properties']['mesh_treatment'] == Parameters.NO_MESH:
            print('\nNo mesh was specified during the generation of case directory.'
                  '\nEnsure you copy a mesh manually before running your case')


