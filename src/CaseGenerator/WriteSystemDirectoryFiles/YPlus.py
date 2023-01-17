from src.CaseGenerator.FileDirectoryIO import WriteHeader


class YPlus:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        yplus = WriteHeader.get_header(version, 'dictionary', 'system', 'yPlus')

        yplus += f'\n'
        yplus += f'yPlus\n'
        yplus += f'{{\n'
        yplus += f'    type            yPlus;\n'
        yplus += f'    libs            (fieldFunctionObjects);\n'
        yplus += f'    writeControl    writeTime;\n'
        yplus += f'    patches         ('
        temp_str = ''
        for boundary in self.properties['dimensionless_coefficients']['wall_boundaries']:
            temp_str += boundary + ' '
        yplus += f'{temp_str[:-1]});\n'
        yplus += f'}}\n'
        yplus += f'\n'
        yplus += f'// ************************************************************************* //\n'
        return yplus
