class ThermophysicalProperties:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_input_file(self):
        mu = str(self.properties['flow_properties']['dimensional_properties']['mu'])
        file_id = self.file_manager.create_file('constant', 'thermophysicalProperties')
        self.file_manager.write_header(file_id, 'dictionary', 'constant', 'thermophysicalProperties')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'thermoType\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            hePsiThermo;\n')
        self.file_manager.write(file_id, '    mixture         pureMixture;\n')
        if self.properties['flow_properties']['const_viscosity']:
            self.file_manager.write(file_id, '    transport       const;\n')
        else:
            self.file_manager.write(file_id, '    transport       sutherland;\n')
        self.file_manager.write(file_id, '    thermo          hConst;\n')
        self.file_manager.write(file_id, '    equationOfState perfectGas;\n')
        self.file_manager.write(file_id, '    specie          specie;\n')
        self.file_manager.write(file_id, '    energy          sensibleInternalEnergy;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'mixture\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    specie\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        molWeight   28.9;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '    thermodynamics\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        Cp          1005;\n')
        self.file_manager.write(file_id, '        Hf          0;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '    transport\n')
        self.file_manager.write(file_id, '    {\n')
        if self.properties['flow_properties']['const_viscosity']:
            self.file_manager.write(file_id, '        mu          ' + mu + ';\n')
            self.file_manager.write(file_id, '        Pr          0.71;\n')
        else:
            self.file_manager.write(file_id, '        As          1.4792e-06;\n')
            self.file_manager.write(file_id, '        Ts          116;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
