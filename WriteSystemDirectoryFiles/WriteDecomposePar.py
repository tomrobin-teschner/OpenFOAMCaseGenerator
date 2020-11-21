class WriteDecomposeParDictionary:
    def __init__(self, file_manager, parallel_properties):
        self.file_manager = file_manager
        self.parallel_properties = parallel_properties

    def write_decompose_par_dict(self):
        file_id = self.file_manager.create_file('system', 'decomposeParDict')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'decomposeParDict')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'numberOfSubdomains ' + str(self.parallel_properties['number_of_processors']) +
                                ';\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'method          scotch;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
