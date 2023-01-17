import os
import distutils.file_util
from src.CaseGenerator.Properties.GlobalVariables import *


class UtilityScripts:
    def __init__(self, properties):
        self.properties = properties

    def get_all_run_content(self):
        all_run = ''
        all_run += f'# !/bin/sh\n'
        all_run += f'cd "${{0%/*}}" || exit  # Run from this directory\n'
        all_run += f'. ${{WM_PROJECT_DIR:?}}/bin/tools/RunFunctions  # Tutorial run functions\n'
        all_run += f'# ------------------------------------------------------------------------------\n'
        all_run += f'\n'

        if self.properties['file_properties']['mesh_treatment'] == Mesh.block_mesh_dict:
            all_run += f'blockMesh\n'
        elif self.properties['file_properties']['mesh_treatment'] == Mesh.snappy_hex_mesh_dict:
            if self.properties['file_properties']['snappyhexmeshdict']['use_blockmeshdict']:
                all_run += f'blockMesh\n'
            if len(self.properties['file_properties']['snappyhexmeshdict']['geometry']) > 0:
                all_run += f'surfaceFeatureExtract\n'
            all_run += f'snappyHexMesh -overwrite\n'

        pre_solver_flag = ''
        post_solver_flag = ''
        if self.properties['parallel_properties']['run_in_parallel']:
            all_run += f'decomposePar\n'
            pre_solver_flag = f'mpirun -np {self.properties["parallel_properties"]["number_of_processors"]} '
            post_solver_flag = f' -parallel'

        all_run += f'{pre_solver_flag}{self.properties["solver_properties"]["solver"].name} {post_solver_flag}\n'
        if self.properties['parallel_properties']['run_in_parallel']:
            all_run += f'reconstructPar\n'

        all_run += f'python3 postProcessing/plotResiduals.py\n'

        if ((self.properties['cutting_planes']['write_cutting_planes'] is True) or
                (self.properties['iso_surfaces']['write_iso_surfaces'] is True)):
            self.copy_PVD_loader_script()

        if self.properties['cutting_planes']['write_cutting_planes'] is True:
            all_run += f'python3 postProcessing/addVTPLoader.py '
            for plane in self.properties['cutting_planes']['location']:
                all_run += f'{plane["name"]} '
            all_run += f'\n'

        if self.properties['iso_surfaces']['write_iso_surfaces'] is True:
            all_run += f'python3 postProcessing/addVTPLoader.py '
            for field in self.properties['iso_surfaces']['flow_variable']:
                all_run += f'isoSurface_{field} '
            all_run += f'\n'

        if self.properties['post_processing']['execute_python_script']:
            for item in self.properties['post_processing']['python_script']:
                src = item['script']
                dst = os.path.join(self.properties['file_properties']['path'], 'postProcessing')
                distutils.file_util.copy_file(src, dst)
                all_run += f'python3 postProcessing/' + os.path.basename(src) + ' '
                for arg in item['arguments']:
                    all_run += f'{arg} '
                all_run += f'\n'
                for requires in item['requires']:
                    src = requires
                    distutils.file_util.copy_file(src, dst)

        all_run += f'\n'
        all_run += f'# ------------------------------------------------------------------------------\n'
        return all_run

    def get_all_clean_content(self):
        all_clean = ''
        all_clean += f'# !/bin/sh\n'
        all_clean += f'cd "${{0%/*}}" || exit  # Run from this directory\n'
        all_clean += f'# ------------------------------------------------------------------------------\n'
        all_clean += f'\n'
        all_clean += f'rm -rf 0.[0-9]* [1-9]* log logs processor*\n'
        all_clean += f'cd postProcessing/\n'
        all_clean += f'find . -type f ! -name \'*.py\' -delete\n'
        all_clean += f'find . -type d -delete\n'
        all_clean += f'cd ../\n'
        all_clean += f'\n'
        all_clean += f'# ------------------------------------------------------------------------------\n'
        return all_clean

    def copy_residual_plotting_script(self):
        src = os.path.join('setups', 'scripts', 'userDefined', 'postProcessing', 'plotResiduals.py')
        dst = os.path.join(self.properties['file_properties']['path'], 'postProcessing')
        distutils.file_util.copy_file(src, dst)

    def copy_PVD_loader_script(self):
        src = os.path.join('setups', 'scripts', 'userDefined', 'postProcessing', 'addVTPLoader.py')
        dst = os.path.join(self.properties['file_properties']['path'], 'postProcessing')
        distutils.file_util.copy_file(src, dst)
