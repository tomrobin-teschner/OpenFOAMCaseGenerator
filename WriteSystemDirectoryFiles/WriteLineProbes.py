class WriteLineProbes:
    def __init__(self, properties, file_manager):
        self.file_manager = file_manager
        self.properties = properties

    def write_line_probes(self):
        file_id = self.file_manager.create_file('system/include', 'lineProbes')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'sampling')
        self.file_manager.write(file_id, '\n')
        for line in self.properties['lineProbes']['location']:
            self.file_manager.write(file_id, line['name'] + '\n')
            self.file_manager.write(file_id, '{\n')
            self.file_manager.write(file_id, '    type                  sets;\n')
            self.file_manager.write(file_id, '    libs                  (sampling);\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    interpolationScheme   cellPoint;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    setFormat             raw;\n')
            self.file_manager.write(file_id, '\n')
            if self.properties['lineProbes']['output_probe_at_every_timestep']:
                self.file_manager.write(file_id, '    writeControl    timeStep;\n')
                self.file_manager.write(file_id, '    writeInterval   1;\n')
            else:
                self.file_manager.write(file_id, '    writeControl    writeTime;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    log                   no;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    sets\n')
            self.file_manager.write(file_id, '    (\n')
            self.file_manager.write(file_id, '        ' + line['name'] + '\n')
            self.file_manager.write(file_id, '        {\n')
            self.file_manager.write(file_id, '            type          uniform;\n')
            self.file_manager.write(file_id, '            axis          xyz;\n')
            self.file_manager.write(file_id, '            start         (' +
                                    str(line['start'][0]) + ' ' + str(line['start'][1]) + ' ' + str(line['start'][2]) +
                                    ');\n')
            self.file_manager.write(file_id, '            end           (' +
                                    str(line['end'][0]) + ' ' + str(line['end'][1]) + ' ' + str(line['end'][2]) +
                                    ');\n')
            self.file_manager.write(file_id, '            nPoints       ' +
                                    str(self.properties['lineProbes']['number_of_samples_on_line']) + ';\n')
            self.file_manager.write(file_id, '        }\n')
            self.file_manager.write(file_id, '    );\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    fields\n')
            self.file_manager.write(file_id, '    (\n')
            for variable in self.properties['lineProbes']['variables_to_monitor']:
                self.file_manager.write(file_id, '        ' + variable + '\n')
            self.file_manager.write(file_id, '    );\n')
            self.file_manager.write(file_id, '}\n')
            self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
