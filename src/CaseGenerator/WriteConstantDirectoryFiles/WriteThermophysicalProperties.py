from src.CaseGenerator.FileDirectoryIO.WriteHeader import WriteHeader

class ThermophysicalProperties:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        is_const_viscosity = self.properties['flow_properties']['const_viscosity']
        mu = str(self.properties['flow_properties']['dimensional_properties']['mu'])
        if is_const_viscosity:
            transport = f'const'
            transport_content = (
                f'        mu          {mu};\n'
                f'        Pr          0.71;\n'
            )
        else:
            transport = f'sutherland'
            transport_content = (
                f'        As          1.4792e-06;\n'
                f'        Ts          116;\n'
            )
        header = WriteHeader.get_header(version, 'dictionary', 'constant', 'thermophysicalProperties')
        
        return (
            f'{header}'
            f'thermoType\n'
            f'{{\n'
            f'    type            hePsiThermo;\n'
            f'    mixture         pureMixture;\n'
            f'    transport       {transport};\n'
            f'    thermo          hConst;\n'
            f'    equationOfState perfectGas;\n'
            f'    specie          specie;\n'
            f'    energy          sensibleInternalEnergy;\n'
            f'}}\n'
            f'\n'
            f'mixture\n'
            f'{{\n'
            f'    specie\n'
            f'    {{\n'
            f'        molWeight   28.9;\n'
            f'    }}\n'
            f'    thermodynamics\n'
            f'    {{\n'
            f'        Cp          1005;\n'
            f'        Hf          0;\n'
            f'    }}\n'
            f'    transport\n'
            f'    {{\n'
            f'{transport_content}'
            f'    }}\n'
            f'}}\n'
            f'\n'
            f'// ************************************************************************* //\n'
        )
