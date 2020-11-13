import FileDirectoryIO.FileManager as IO
import GlobalVariables as Parameters


class TurbulencePropertiesFile:
    def __init__(self, file_manager, simulation_type):
        self.file_manager = file_manager
        self.simulation_type = simulation_type

    def write_input_file(self):
        file_id = self.file_manager.create_file('constant', 'turbulenceProperties')
        self.file_manager.write_header(file_id, 'dictionary', 'constant', 'turbulenceProperties')
        self.file_manager.write(file_id, '\n')
        if self.simulation_type == Parameters.LAMINAR:
            self.file_manager.write(file_id, 'simulationType laminar;\n')
        elif self.simulation_type == Parameters.RANS:
            self.file_manager.write(file_id, 'simulationType RAS;\n')
        elif self.simulation_type == Parameters.LES:
            self.file_manager.write(file_id, 'simulationType LES;\n')
        self.file_manager.write(file_id, '\n')
        if self.simulation_type != Parameters.LAMINAR:
            if self.simulation_type == Parameters.RANS:
                self.file_manager.write(file_id, 'RAS\n{\n')
                self.file_manager.write(file_id, '    RASModel        kOmegaSST;\n')
                self.file_manager.write(file_id, '\n')
                self.file_manager.write(file_id, '    turbulence      on;\n')
                self.file_manager.write(file_id, '\n')
                self.file_manager.write(file_id, '    printCoeffs     on;\n')
            if self.simulation_type == Parameters.LES:
                self.file_manager.write(file_id, 'LES\n{\n')
                self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '}\n\n')
        self.file_manager.write(file_id, '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
