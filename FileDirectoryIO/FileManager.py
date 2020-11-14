import os


class FileManager:
    def __init__(self, file_properties):
        self.file_properties = file_properties

    def create_directory_structure(self):
        self.__create_directory(os.path.join(self.file_properties['path']))
        self.__create_directory(os.path.join(self.file_properties['path'], '0'))
        self.__create_directory(os.path.join(self.file_properties['path'], 'constant'))
        self.__create_directory(os.path.join(self.file_properties['path'], 'system'))
        self.__create_case_file()

    def __create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __create_case_file(self):
        file_id = open(os.path.join(self.file_properties['path'], self.file_properties['case_name'] + '.foam'), 'w')
        file_id.close()

    def create_file(self, folder, file_name):
        file_id = open(os.path.join(self.file_properties['path'], folder, file_name), 'w')
        return file_id

    def close_file(self, file_id):
        file_id.close()

    def write(self, file_id, message):
        file_id.write(message)

    def write_header(self, file_id, class_type, location, object_type):
        file_id.write('/*--------------------------------*- C++ -*----------------------------------*\\\n')
        file_id.write('| =========                 |                                                 |\n')
        file_id.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        file_id.write('|  \\\    /   O peration     | Version:  ' + self.file_properties['version'] + '                                 |\n')
        file_id.write('|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |\n')
        file_id.write('|    \\\/     M anipulation  |                                                 |\n')
        file_id.write('\*---------------------------------------------------------------------------*/\n')
        file_id.write('FoamFile\n')
        file_id.write('{\n')
        file_id.write('    version     2.0;\n')
        file_id.write('    format      ascii;\n')
        file_id.write('    class       ' + class_type + ';\n')
        file_id.write('    location    "' + location + '";\n')
        file_id.write('    object      ' + object_type + ';\n')
        file_id.write('}\n')
        file_id.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')

    def write_all_run_file(self):
        file_id = self.create_file('', 'Allrun')
        self.write(file_id, '# !/bin/sh\n')
        self.write(file_id, 'cd "${0%/*}" || exit  # Run from this directory\n')
        self.write(file_id, '. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions  # Tutorial run functions\n')
        self.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.write(file_id, '\n')
        self.write(file_id, 'runApplication $(getApplication)\n')
        self.write(file_id, 'foamLog log.*\n')
        self.write(file_id, '\n')
        self.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.close_file(file_id)

    def write_all_clean_file(self):
        file_id = self.create_file('', 'Allclean')
        self.write(file_id, '# !/bin/sh\n')
        self.write(file_id, 'cd "${0%/*}" || exit  # Run from this directory\n')
        self.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.write(file_id, '\n')
        self.write(file_id, 'rm -rf 0.* [1-9]* log.*\n')
        self.write(file_id, '\n')
        self.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.close_file(file_id)
