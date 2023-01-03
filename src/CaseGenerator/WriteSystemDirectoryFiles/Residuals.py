from src.CaseGenerator.FileDirectoryIO import WriteHeader


class Residuals:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        residuals = WriteHeader.get_header(version, 'dictionary', 'system', 'residuals')
        residuals += f'\n'
        residuals += f'residuals\n'
        residuals += f'{{\n'
        residuals += f'    type            solverInfo;\n'
        residuals += f'    libs            (utilityFunctionObjects);\n'
        residuals += f'    fields          (".*");\n'
        residuals += f'}}\n'
        residuals += f'\n'
        residuals += f'// ************************************************************************* //\n'
        return residuals
