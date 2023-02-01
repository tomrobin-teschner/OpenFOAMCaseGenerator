from src.CaseGenerator.FileDirectoryIO.WriteHeader import WriteHeader


class TransportPropertiesFile:
    def __init__(self, properties):
        self.properties = properties
    
    def get_file_content(self):
        version = self.properties['file_properties']['version']
        nu = self.properties['flow_properties']['dimensional_properties']['material_properties']['nu']
        header = WriteHeader.get_header(version, 'dictionary', 'constant', 'transportProperties')

        return (
            f'{header}'
            f'transportModel  Newtonian;\n'
            f'\n'
            f'nu              {str(nu)};\n'
            f'\n'
            f'// ************************************************************************* //\n'
        )
