class WritePointProbes:
    def __init__(self, properties, file_manager):
        self.file_manager = file_manager
        self.properties = properties

    def write_point_probes(self):
        file_id = self.file_manager.create_file('system/include', 'pointProbes')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'sampling')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'pointProbes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            probes;\n')
        self.file_manager.write(file_id, '    libs            (fieldFunctionObjects);\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    writeControl    timeStep;\n')
        self.file_manager.write(file_id, '    writeInterval   1;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    log             no;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    probeLocations\n')
        self.file_manager.write(file_id, '    (\n')
        for point in self.properties['pointProbes']['location']:
            self.file_manager.write(file_id, '        (' +
                                    str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + ' ' + ')\n')
        self.file_manager.write(file_id, '    );\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    fields\n')
        self.file_manager.write(file_id, '    (\n')
        for variable in self.properties['pointProbes']['variables_to_monitor']:
            self.file_manager.write(file_id, '        ' + variable + '\n')
        self.file_manager.write(file_id, '    );\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
