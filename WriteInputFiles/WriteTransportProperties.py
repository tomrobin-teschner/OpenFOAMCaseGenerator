import FileDirectoryIO.FileManager as IO


class TransportPropertiesFile:
    def __init__(self, file_manager, simulation_type):
        self.file_manager = file_manager
        self.simulation_type = simulation_type

    def write_input_file(self):
        file_id = self.file_manager.create_file('constant', 'transportProperties')
        self.file_manager.write_header(file_id, 'dictionary', 'constant', 'transportProperties')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'transportModel  Newtonian;\n\n')
        self.file_manager.write(file_id, 'nu              ' + str(self.simulation_type['nu']) + ';\n\n')
        self.file_manager.write(file_id, '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
