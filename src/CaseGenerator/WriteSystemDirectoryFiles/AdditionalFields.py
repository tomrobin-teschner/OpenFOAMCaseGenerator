from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator.FileDirectoryIO import WriteHeader


class AdditionalFields:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        fields = WriteHeader.get_header(version, 'dictionary', 'system', 'fields')

        if self.properties['additional_fields']['write_additional_fields']:
            for field in self.properties['additional_fields']['fields']:
                fields += f'{field.name}\n'
                fields += f'{{\n'
                fields += f'    type            {field.name};\n'
                fields += f'    libs            (fieldFunctionObjects);\n'
                fields += f'\n'
                fields += f'    writeControl    writeTime;\n'
                fields += f'\n'
                fields += f'    log             no;\n'
                fields += f'}}\n'
                fields += f'\n'
        fields += f'// ************************************************************************* //\n'
        return fields
