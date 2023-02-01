from src.CaseGenerator.FileDirectoryIO import WriteHeader


class PressureCoefficient:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        velocity_vector = self.properties['flow_properties']['dimensional_properties']['velocity_vector']
        rho = self.properties['flow_properties']['dimensional_properties']['material_properties']['rho']
        pressure = self.properties['flow_properties']['dimensional_properties']['material_properties']['p']
        velocity = ('(' + str(velocity_vector[0]) + ' ' + str(velocity_vector[1]) + ' ' + str(velocity_vector[2]) + ')')
        
        version = self.properties['file_properties']['version']
        cp = WriteHeader.get_header(version, 'dictionary', 'system', 'pressureCoefficient')

        cp += f'\n'
        cp += f'pressureCoefficient\n'
        cp += f'{{\n'
        cp += f'    type            pressure;\n'
        cp += f'    libs            (fieldFunctionObjects);\n'
        cp += f'\n'
        cp += f'    writeControl    writeTime;\n'
        cp += f'    mode            staticCoeff;\n'
        cp += f'    result          cp;\n'
        cp += f'\n'
        cp += f'    rho             rhoInf;\n'
        cp += f'    rhoInf          {rho};\n'
        cp += f'    pInf            {pressure};\n'
        cp += f'    UInf            {velocity};\n'
        cp += f'}}\n'
        cp += f'\n'
        cp += f'// ************************************************************************* //\n'
        return cp
