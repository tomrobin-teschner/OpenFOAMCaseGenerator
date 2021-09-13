class WritePressureCoefficient:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_force_coefficients(self):
        velocity_vector = self.properties['flow_properties']['dimensional_properties']['velocity_vector']
        rho = self.properties['flow_properties']['dimensional_properties']['rho']
        pressure = self.properties['flow_properties']['dimensional_properties']['p']
        velocity = ('(' + str(velocity_vector[0]) + ' ' + str(velocity_vector[1]) + ' ' + str(velocity_vector[2]) + ')')
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
        self.file_manager.write(file_id, '    rhoInf          ' + str(rho) + ';\n')
        self.file_manager.write(file_id, '    pInf            ' + str(pressure) + ';\n')
        self.file_manager.write(file_id, '    UInf            ' + velocity + ';\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
