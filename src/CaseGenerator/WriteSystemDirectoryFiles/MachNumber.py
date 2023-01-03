from src.CaseGenerator.FileDirectoryIO import WriteHeader


class MachNumber:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        mach_number = WriteHeader.get_header(version, 'dictionary', 'system', 'MachNo')
        mach_number += f'\n'
        mach_number += f'MachNo\n'
        mach_number += f'{{\n'
        mach_number += f'    type            MachNo;\n'
        mach_number += f'    libs            (fieldFunctionObjects);\n'
        mach_number += f'    writeControl    writeTime;\n'
        mach_number += f'}}\n'
        mach_number += f'\n'
        mach_number += f'// ************************************************************************* //\n'
        return mach_number
