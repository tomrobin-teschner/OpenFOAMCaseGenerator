class WriteIsoSurfaces:
    def __init__(self, properties, file_manager):
        self.file_manager = file_manager
        self.properties = properties

    def write_iso_surfaces(self):
        file_id = self.file_manager.create_file('system/include', 'isoSurfaces')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'sampling')
        self.file_manager.write(file_id, '\n')
        for index in range(0, len(self.properties['iso_surfaces']['flow_variable'])):
            self.__write_iso_surfaces_for_field_at_index(file_id, index)
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')

    def __write_iso_surfaces_for_field_at_index(self, file_id, index):
        field = self.properties['iso_surfaces']['flow_variable'][index]
        value = self.properties['iso_surfaces']['iso_value'][index]

        self.file_manager.write(file_id, 'isoSurface_' + field + '\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type                  surfaces;\n')
        self.file_manager.write(file_id, '    libs                  (sampling);\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    interpolationScheme   cellPoint;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    surfaceFormat         vtk;\n')
        self.file_manager.write(file_id, '\n')
        if self.properties['iso_surfaces']['output_iso_surfaces_at_every_timestep']:
            self.file_manager.write(file_id, '    writeControl          timeStep;\n')
            self.file_manager.write(file_id, '    writeInterval         1;\n')
        else:
            self.file_manager.write(file_id, '    writeControl          writeTime;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    log                   no;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    surfaces\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        isoSurface_' + field + '\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            type          isoSurface;\n')
        self.file_manager.write(file_id, '            isoField      ' + field + ';\n')
        self.file_manager.write(file_id, '            isoValue      ' + str(value) + ';\n')
        self.file_manager.write(file_id, '            interpolate   true;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    fields\n')
        self.file_manager.write(file_id, '    (\n')
        self.file_manager.write(file_id, '        ' + field + '\n')
        for additional_field in self.properties['iso_surfaces']['additional_field_to_write']:
            self.file_manager.write(file_id, '        ' + additional_field + '\n')
        self.file_manager.write(file_id, '    );\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
