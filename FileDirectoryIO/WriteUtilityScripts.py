import os


class WriteUtilityScripts:
    def __init__(self, file_properties, file_manager, solver_properties, parallel_properties):
        self.file_properties = file_properties
        self.file_manager = file_manager
        self.solver_properties = solver_properties
        self.parallel_properties = parallel_properties

    def write_all_run_file(self):
        file_id = self.file_manager.create_file('', 'Allrun')
        self.file_manager.write(file_id, '# !/bin/sh\n')
        self.file_manager.write(file_id, 'cd "${0%/*}" || exit  # Run from this directory\n')
        self.file_manager.write(file_id, '. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions  # Tutorial run functions\n')
        self.file_manager.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.file_manager.write(file_id, '\n')
        if self.parallel_properties['run_in_parallel']:
            self.file_manager.write(file_id, 'decomposePar\n')
            self.file_manager.write(file_id, 'foamJob -parallel ' + self.solver_properties['solver'] + '\n')
        else:
            self.file_manager.write(file_id, 'foamJob ' + self.solver_properties['solver'] + '\n')
        self.file_manager.write(file_id, 'foamLog log\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.file_manager.close_file(file_id)

    def write_all_clean_file(self):
        file_id = self.file_manager.create_file('', 'Allclean')
        self.file_manager.write(file_id, '# !/bin/sh\n')
        self.file_manager.write(file_id, 'cd "${0%/*}" || exit  # Run from this directory\n')
        self.file_manager.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'rm -rf 0.[0-9]* [1-9]* log logs postProcessing processor*\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '# ------------------------------------------------------------------------------\n')
        self.file_manager.close_file(file_id)
