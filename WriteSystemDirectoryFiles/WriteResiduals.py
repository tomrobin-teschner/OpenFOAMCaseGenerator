class WriteResiduals:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def write_residuals(self):
        file_id = self.file_manager.create_file('system/include', 'residuals')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'residuals')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'residuals\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            solverInfo;\n')
        self.file_manager.write(file_id, '    libs            (utilityFunctionObjects);\n')
        self.file_manager.write(file_id, '    fields          (".*");\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
