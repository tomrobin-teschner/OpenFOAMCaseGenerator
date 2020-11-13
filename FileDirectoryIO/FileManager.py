import os


class FileManager:
    def __init__(self, case_name, path, version):
        self.case_name = case_name
        self.path = path
        self.version = version

    def create_directory_structure(self):
        self.__create_directory(os.path.join(self.path, self.case_name))
        self.__create_directory(os.path.join(self.path, self.case_name, '0'))
        self.__create_directory(os.path.join(self.path, self.case_name, 'constant'))
        self.__create_directory(os.path.join(self.path, self.case_name, 'system'))
        self.__create_case_file()

    def __create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __create_case_file(self):
        file_id = open(os.path.join(self.path, self.case_name, self.case_name + '.foam'), 'w')
        file_id.close()

    def create_file(self, folder, file_name):
        file_id = open(os.path.join(self.path, self.case_name, folder, file_name), 'w')
        return file_id

    def close_file(self, file_id):
        file_id.close();

    def write(self, file_id, message):
        file_id.write(message)

    def write_header(self, file_id, class_type, location, object):
        file_id.write('/*--------------------------------*- C++ -*----------------------------------*\\\n')
        file_id.write('| =========                 |                                                 |\n')
        file_id.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        file_id.write('|  \\\    /   O peration     | Version:  ' + self.version + '                                 |\n')
        file_id.write('|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |\n')
        file_id.write('|    \\\/     M anipulation  |                                                 |\n')
        file_id.write('\*---------------------------------------------------------------------------*/\n')
        file_id.write('FoamFile\n')
        file_id.write('{\n')
        file_id.write('    version     2.0;\n')
        file_id.write('    format      ascii;\n')
        file_id.write('    class       ' + class_type + ';\n')
        file_id.write('    location    "' + location + '";\n')
        file_id.write('    object      ' + object + ';\n')
        file_id.write('}\n')
        file_id.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')
