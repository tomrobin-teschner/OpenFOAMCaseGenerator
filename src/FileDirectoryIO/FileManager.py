import os
import distutils.dir_util
import distutils.file_util
from src.Properties import GlobalVariables as Parameters


class FileManager:
    def __init__(self, properties):
        self.properties = properties

    def copy_mesh_to_destination(self):
        if self.properties['file_properties']['mesh_treatment'] == Parameters.BLOCK_MESH_DICT:
            src = os.path.join(self.properties['file_properties']['blockmeshdict_directory'], 'blockMeshDict')
            dst = os.path.join(self.properties['file_properties']['path'], 'system', 'blockMeshDict')
            self.copy_file(src, dst)

        elif self.properties['file_properties']['mesh_treatment'] == Parameters.SNAPPY_HEX_MESH_DICT:
            snappy_properties = self.properties['file_properties']['snappyhexmeshdict']
            system_dst = os.path.join(self.properties['file_properties']['path'], 'system')

            # copy snappyHexMeshDict file
            snappy_src = os.path.join(snappy_properties['snappyhexmesh_directory'], 'snappyHexMeshDict')
            self.copy_file(snappy_src, system_dst)

            # check if a blockMeshDict file exists and copy it into the case if so
            block_mesh_src = os.path.join(snappy_properties['blockmeshdict_directory'], 'blockMeshDict')
            use_block_mesh = self.file_exists(block_mesh_src)
            self.properties['file_properties']['snappyhexmeshdict']['use_blockmeshdict'] = use_block_mesh
            if use_block_mesh:
                self.copy_file(block_mesh_src, system_dst)

            # check if a polyMesh directory exists and copy it into the case if so
            poly_mesh_src = os.path.join(snappy_properties['snappyhexmesh_directory'], 'polymesh_directory')
            if self.directory_exist(poly_mesh_src):
                poly_mesh_dst = os.path.join(self.properties['file_properties']['path'], 'constant', 'polyMesh')
                self.copy_directory(poly_mesh_src, poly_mesh_dst)

            # check if a geometry file (or files) has/have been specified, copy into triSurface folder if so
            geometries = snappy_properties['geometry']
            geometry_dst = os.path.join(self.properties['file_properties']['path'], 'constant', 'triSurface')

            if len(geometries) > 0:
                self.__create_directory(geometry_dst)

            for geometry in geometries:
                if self.file_exists(geometry):
                    self.copy_file(geometry, geometry_dst)

        elif self.properties['file_properties']['mesh_treatment'] == Parameters.POLY_MESH:
            src = os.path.join(self.properties['file_properties']['polymesh_directory'], 'polyMesh')
            dst = os.path.join(self.properties['file_properties']['path'], 'constant', 'polyMesh')
            self.copy_directory(src, dst)

    def create_directory_structure(self):
        self.__create_directory(os.path.join(self.properties['file_properties']['path']))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], '0'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'constant'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'system'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'system/include'))
        self.__create_directory(os.path.join(self.properties['file_properties']['path'], 'postProcessing'))
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

    @staticmethod
    def copy_directory(src, dst):
        distutils.dir_util.copy_tree(src, dst)

    @staticmethod
    def copy_file(src, dst):
        distutils.file_util.copy_file(src, dst)

    @staticmethod
    def file_exists(file):
        return os.path.isfile(file)

    @staticmethod
    def directory_exist(directory):
        return os.path.isdir(directory)

    def __create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __create_case_file(self):
        file_id = open(os.path.join(self.properties['file_properties']['path'],
                                    self.properties['file_properties']['case_name'] + '.foam'), 'w')
        file_id.close()
