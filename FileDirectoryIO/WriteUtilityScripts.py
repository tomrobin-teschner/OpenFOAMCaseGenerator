import GlobalVariables as Parameters


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
        if self.properties['parallel_properties']['run_in_parallel']:
            self.file_manager.write(file_id, 'decomposePar\n')
            if self.properties['solver_properties']['solver'] == Parameters.simpleFoam:
                self.file_manager.write(file_id, 'foamJob -parallel simpleFoam\n')
            elif self.properties['solver_properties']['solver'] == Parameters.icoFoam:
                self.file_manager.write(file_id, 'foamJob -parallel icoFoam\n')
            elif self.properties['solver_properties']['solver'] == Parameters.pisoFoam:
                self.file_manager.write(file_id, 'foamJob -parallel pisoFoam\n')
            elif self.properties['solver_properties']['solver'] == Parameters.pimpleFoam:
                self.file_manager.write(file_id, 'foamJob -parallel pimpleFoam\n')
        else:
            if self.properties['solver_properties']['solver'] == Parameters.simpleFoam:
                self.file_manager.write(file_id, 'foamJob simpleFoam\n')
            elif self.properties['solver_properties']['solver'] == Parameters.icoFoam:
                self.file_manager.write(file_id, 'foamJob icoFoam\n')
            elif self.properties['solver_properties']['solver'] == Parameters.pisoFoam:
                self.file_manager.write(file_id, 'foamJob pisoFoam\n')
            elif self.properties['solver_properties']['solver'] == Parameters.pimpleFoam:
                self.file_manager.write(file_id, 'foamJob pimpleFoam\n')
        self.file_manager.write(file_id, 'foamLog log\n')
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
