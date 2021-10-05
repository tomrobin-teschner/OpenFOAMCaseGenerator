import os
import distutils.file_util
from src.Properties import GlobalVariables as Parameters


class WriteUtilityScripts:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_all_run_file(self):
        file_id = self.file_manager.create_file('', 'Allrun')
        self.file_manager.write(file_id, '# !/bin/sh\n')
        self.file_manager.write(file_id, 'cd "${0%/*}" || exit  # Run from this directory\n')
        self.file_manager.write(file_id, '. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions  # Tutorial run functions\n')
        self.file_manager.write(file_id,
                                '# ------------------------------------------------------------------------------\n')
        self.file_manager.write(file_id, '\n')

        if self.properties['file_properties']['mesh_treatment'] == Parameters.BLOCK_MESH_DICT:
            self.file_manager.write(file_id, 'blockMesh\n')
        elif self.properties['file_properties']['mesh_treatment'] == Parameters.BLOCK_MESH_AND_SNAPPY_HEX_MESH_DICT:
            self.file_manager.write(file_id, 'blockMesh\n')
            self.file_manager.write(file_id, 'snappyHexMesh\n')

        pre_solver_flag = ''
        post_solver_flag = ''
        if self.properties['parallel_properties']['run_in_parallel']:
            self.file_manager.write(file_id, 'decomposePar\n')
            pre_solver_flag = 'mpirun -np ' + str(self.properties['parallel_properties']['number_of_processors']) + ' '
            post_solver_flag = ' -parallel'

        if self.properties['solver_properties']['solver'] == Parameters.simpleFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'simpleFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.icoFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'icoFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.pisoFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'pisoFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.pimpleFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'pimpleFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.rhoCentralFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'rhoCentralFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.rhoSimpleFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'rhoSimpleFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.rhoPimpleFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'rhoPimpleFoam' + post_solver_flag + '\n')
        elif self.properties['solver_properties']['solver'] == Parameters.sonicFoam:
            self.file_manager.write(file_id, pre_solver_flag + 'sonicFoam' + post_solver_flag + '\n')

        if self.properties['parallel_properties']['run_in_parallel']:
            self.file_manager.write(file_id, 'reconstructPar\n')

        self.file_manager.write(file_id, 'python3 postProcessing/plotResiduals.py\n')

        if ((self.properties['cutting_planes']['write_cutting_planes'] is True) or
                (self.properties['iso_surfaces']['write_iso_surfaces'] is True)):
            self.copy_PVD_loader_script()

        if self.properties['cutting_planes']['write_cutting_planes'] is True:
            self.file_manager.write(file_id, 'python3 postProcessing/addVTPLoader.py ')
            for plane in self.properties['cutting_planes']['location']:
                self.file_manager.write(file_id, plane['name'] + ' ')
            self.file_manager.write(file_id, '\n')

        if self.properties['iso_surfaces']['write_iso_surfaces'] is True:
            self.file_manager.write(file_id, 'python3 postProcessing/addVTPLoader.py ')
            for field in self.properties['iso_surfaces']['flow_variable']:
                self.file_manager.write(file_id, 'isoSurface_' + field + ' ')
            self.file_manager.write(file_id, '\n')

        if self.properties['post_processing']['execute_python_scrip']:
            for item in self.properties['post_processing']['python_script']:
                src = item['script']
                dst = os.path.join(self.properties['file_properties']['path'], 'postProcessing')
                distutils.file_util.copy_file(src, dst)
                self.file_manager.write(file_id, 'python3 postProcessing/' + os.path.basename(src) + '\n')
                for requires in item['requires']:
                    src = requires
                    distutils.file_util.copy_file(src, dst)


        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '# ------------------------------------------------------------------------------\n')
        self.file_manager.close_file(file_id)

    def write_all_clean_file(self):
        file_id = self.file_manager.create_file('', 'Allclean')
        self.file_manager.write(file_id, '# !/bin/sh\n')
        self.file_manager.write(file_id, 'cd "${0%/*}" || exit  # Run from this directory\n')
        self.file_manager.write(file_id,
                                '# ------------------------------------------------------------------------------\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'rm -rf 0.[0-9]* [1-9]* log logs processor*\n')
        self.file_manager.write(file_id, 'cd postProcessing/\n')
        self.file_manager.write(file_id, 'find . -type f ! -name \'*.py\' -delete\n')
        self.file_manager.write(file_id, 'find . -type d -delete\n')
        self.file_manager.write(file_id, 'cd ../\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '# ------------------------------------------------------------------------------\n')
        self.file_manager.close_file(file_id)

    def copy_residual_plotting_script(self):
        if not os.path.exists(os.path.join(self.properties['file_properties']['path'], 'postProcessing')):
            os.makedirs(os.path.join(self.properties['file_properties']['path'], 'postProcessing'))
        src = os.path.join('examples', 'scripts', 'userDefined', 'postProcessing', 'plotResiduals.py')
        dst = os.path.join(self.properties['file_properties']['path'], 'postProcessing')
        distutils.file_util.copy_file(src, dst)

    def copy_PVD_loader_script(self):
        if not os.path.exists(os.path.join(self.properties['file_properties']['path'], 'postProcessing')):
            os.makedirs(os.path.join(self.properties['file_properties']['path'], 'postProcessing'))
        src = os.path.join('examples', 'scripts', 'userDefined', 'postProcessing', 'addVTPLoader.py')
        dst = os.path.join(self.properties['file_properties']['path'], 'postProcessing')
        distutils.file_util.copy_file(src, dst)
