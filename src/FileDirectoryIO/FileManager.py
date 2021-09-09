import os
import distutils.dir_util
import distutils.file_util
from input import GlobalVariables as Parameters


class FileManager:
    def __init__(self, properties):
        self.properties = properties

    def copy_mesh_to_destination(self):
        if self.properties['file_properties']['mesh_treatment'] == Parameters.BLOCK_MESH_DICT:
            self.__copy_block_mesh_dict()

        elif self.properties['file_properties']['mesh_treatment'] == Parameters.BLOCK_MESH_AND_SNAPPY_HEX_MESH_DICT:
            self.__copy_block_mesh_dict()
            self.__copy_snappy_hex_mesh_dict()

        elif self.properties['file_properties']['mesh_treatment'] == Parameters.POLY_MESH:
            self.__copy_poly_mesh_dict()

    def create_directory_structure(self):
        self.__create_directory(os.path.join(self.properties['file_properties']['path']))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], '0'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'constant'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'system'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'system/include'))
        self.__create_case_file()

    def create_file(self, folder, file_name):
        file_id = open(os.path.join(self.properties['file_properties']['path'], folder, file_name), 'w')
        return file_id

    def close_file(self, file_id):
        file_id.close()

    def write(self, file_id, message):
        file_id.write(message)

    def write_header(self, file_id, class_type, location, object_type):
        file_id.write('/*--------------------------------*- C++ -*----------------------------------*\\\n')
        file_id.write('| =========                 |                                                 |\n')
        file_id.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        file_id.write('|  \\\    /   O peration     | Version:  ' + self.properties['file_properties']['version'] + '                                 |\n')
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

    def get_version(self):
        return self.properties['file_properties']['version']

    def copy_directory(self, src, dst):
        distutils.dir_util.copy_tree(src, dst)

    def copy_file(self, src, dst):
        distutils.file_util.copy_file(src, dst)

    def __copy_block_mesh_dict(self):
        src = os.path.join(self.properties['file_properties']['blockmeshdict_directory'], 'blockMeshDict')
        dst = os.path.join(self.properties['file_properties']['path'], 'system', 'blockMeshDict')
        self.copy_file(src, dst)

    def __copy_snappy_hex_mesh_dict(self):
        src = os.path.join(self.properties['file_properties']['snappyhexmeshdict_directory'], 'snappyHexMeshDict')
        dst = os.path.join(self.properties['file_properties']['path'], 'system', 'snappyHexMeshDict')
        self.copy_file(src, dst)

    def __copy_poly_mesh_dict(self):
        src = os.path.join(self.properties['file_properties']['polymesh_directory'], 'polyMesh')
        dst = os.path.join(self.properties['file_properties']['path'], 'constant', 'polyMesh')
        self.copy_directory(src, dst)

    def __create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __create_case_file(self):
        file_id = open(os.path.join(self.properties['file_properties']['path'],
                                    self.properties['file_properties']['case_name'] + '.foam'), 'w')
        file_id.close()
