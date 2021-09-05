class TransportPropertiesFile:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_input_file(self):
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        file_id = self.file_manager.create_file('constant', 'transportProperties')
        self.file_manager.write_header(file_id, 'dictionary', 'constant', 'transportProperties')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'transportModel  Newtonian;\n\n')
        self.file_manager.write(file_id, 'nu              ' + str(nu) + ';\n\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
