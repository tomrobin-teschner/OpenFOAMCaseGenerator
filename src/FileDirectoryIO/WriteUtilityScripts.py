import os
import distutils.file_util
from src import GlobalVariables as Parameters


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

        self.file_manager.write(file_id, 'python3 plotResiduals.py\n')
        if self.properties['cutting_planes']['write_cutting_planes'] is True:
            self.copy_PVD_loader_script()
            self.file_manager.write(file_id, 'python3 addVTPLoader.py ')
            for plane in self.properties['cutting_planes']['location']:
                self.file_manager.write(file_id, plane['name'] + ' ')
            self.file_manager.write(file_id, '\n')

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
        self.file_manager.write(file_id, 'rm -rf 0.[0-9]* [1-9]* log logs postProcessing processor*\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '# ------------------------------------------------------------------------------\n')
        self.file_manager.close_file(file_id)

    def copy_residual_plotting_script(self):
        src = os.path.join('utilityScripts', 'plotResiduals.py')
        dst = self.properties['file_properties']['path']
        distutils.file_util.copy_file(src, dst)

    def copy_PVD_loader_script(self):
        src = os.path.join('utilityScripts', 'addVTPLoader.py')
        dst = self.properties['file_properties']['path']
        distutils.file_util.copy_file(src, dst)
