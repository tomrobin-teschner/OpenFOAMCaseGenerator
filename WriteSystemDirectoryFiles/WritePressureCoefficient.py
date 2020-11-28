class WritePressureCoefficient:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_force_coefficients(self):
        velocity = ('(' + str(self.properties['flow_properties']['inlet_velocity'][0]) + ' ' +
                    str(self.properties['flow_properties']['inlet_velocity'][1]) + ' ' +
                    str(self.properties['flow_properties']['inlet_velocity'][2]) + ')')
        file_id = self.file_manager.create_file('system/include', 'pressureCoefficient')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'pressureCoefficient')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'pressureCoefficient\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            pressure;\n')
        self.file_manager.write(file_id, '    libs            (fieldFunctionObjects);\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    writeControl    writeTime;\n')
        self.file_manager.write(file_id, '    mode            staticCoeff;\n')
        self.file_manager.write(file_id, '    result          cp;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    rho             rhoInf;\n')
        self.file_manager.write(file_id, '    rhoInf          1;\n')
        self.file_manager.write(file_id, '    pInf            0;\n')
        self.file_manager.write(file_id, '    UInf            ' + velocity + ';\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
