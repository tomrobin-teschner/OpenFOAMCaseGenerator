class WriteYPlus:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_y_plus(self):
        file_id = self.file_manager.create_file('system/include', 'yPlus')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'yPlus')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'yPlus\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            yPlus;\n')
        self.file_manager.write(file_id, '    libs            (fieldFunctionObjects);\n')
        self.file_manager.write(file_id, '    writeControl    writeTime;\n')
        if len(self.properties['dimensionless_coefficients']['wall_boundaries']) == 1:
            self.file_manager.write(file_id, '    patches         (' +
                                    self.properties['dimensionless_coefficients']['wall_boundaries'][0] + ');\n')
        else:
            self.file_manager.write(file_id, '    patches         (')
            temp_str = ''
            for boundary in self.properties['dimensionless_coefficients']['wall_boundaries']:
                temp_str += boundary + ' '
            self.file_manager.write(file_id, temp_str[:-1] + ');\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
