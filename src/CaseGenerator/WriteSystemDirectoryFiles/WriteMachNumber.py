class WriteMachNumber:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_mach_number(self):
        file_id = self.file_manager.create_file('system/include', 'MachNo')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'MachNo')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'MachNo\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            MachNo;\n')
        self.file_manager.write(file_id, '    libs            (fieldFunctionObjects);\n')
        self.file_manager.write(file_id, '    writeControl    writeTime;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
