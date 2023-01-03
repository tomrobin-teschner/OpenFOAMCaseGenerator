class WriteCuttingPlanes:
    def __init__(self, properties, file_manager):
        self.file_manager = file_manager
        self.properties = properties

    def write_cutting_planes(self):
        file_id = self.file_manager.create_file('system/include', 'cuttingPlanes')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'sampling')
        self.file_manager.write(file_id, '\n')
        for line in self.properties['cutting_planes']['location']:
            self.file_manager.write(file_id, line['name'] + '\n')
            self.file_manager.write(file_id, '{\n')
            self.file_manager.write(file_id, '    type                  surfaces;\n')
            self.file_manager.write(file_id, '    libs                  (sampling);\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    interpolationScheme   cellPoint;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    surfaceFormat         vtk;\n')
            self.file_manager.write(file_id, '\n')
            if self.properties['cutting_planes']['output_cutting_plane_at_every_timestep']:
                self.file_manager.write(file_id, '    writeControl    timeStep;\n')
                self.file_manager.write(file_id, '    writeInterval   1;\n')
            else:
                self.file_manager.write(file_id, '    writeControl    writeTime;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    log                   no;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    surfaces\n')
            self.file_manager.write(file_id, '    {\n')
            self.file_manager.write(file_id, '        ' + line['name'] + '\n')
            self.file_manager.write(file_id, '        {\n')
            self.file_manager.write(file_id, '            type          cuttingPlane;\n')
            self.file_manager.write(file_id, '            planeType     pointAndNormal;\n')
            self.file_manager.write(file_id, '            pointAndNormalDict\n')
            self.file_manager.write(file_id, '            {\n')
            self.file_manager.write(file_id, '                point     (' +
                                    str(line['origin'][0]) + ' ' + str(line['origin'][1]) + ' ' +
                                    str(line['origin'][2]) + ');\n')
            self.file_manager.write(file_id, '                normal    (' +
                                    str(line['normal'][0]) + ' ' + str(line['normal'][1]) + ' ' +
                                    str(line['normal'][2]) + ');\n')
            self.file_manager.write(file_id, '            }\n')
            self.file_manager.write(file_id, '            interpolate   true;\n')
            self.file_manager.write(file_id, '        }\n')
            self.file_manager.write(file_id, '    }\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    fields\n')
            self.file_manager.write(file_id, '    (\n')
            for variable in self.properties['cutting_planes']['variables_to_monitor']:
                self.file_manager.write(file_id, '        ' + variable + '\n')
            self.file_manager.write(file_id, '    );\n')
            self.file_manager.write(file_id, '}\n')
            self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
