from src.CaseGenerator.FileDirectoryIO import WriteHeader

class DecomposeParDictionary:
    def __init__(self, properties):
        self.properties = properties

    def get_decompose_par_dict(self):
        version = self.properties['file_properties']['version']
        num_processors = self.properties['parallel_properties']['number_of_processors']
        header = WriteHeader.get_header(version, 'dictionary', 'system', 'decomposeParDict')
        return (
            f'{header}'
            f'numberOfSubdomains {num_processors};\n'
            f'\n'
            f'method          scotch;\n'
            f'\n'
            f'// ************************************************************************* //\n'
        )