import GlobalVariables as Parameters


class ControlDictFile:
    def __init__(self, file_manager, solver_properties):
        self.file_manager = file_manager
        self.solver_properties = solver_properties

    def write_input_file(self):
        file_id = self.file_manager.create_file('system', 'controlDict')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'controlDict')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'application       ' + self.solver_properties['solver'] + ';\n\n')
        self.file_manager.write(file_id, 'startFrom         startTime;\n\n')
        self.file_manager.write(file_id, 'startTime         ' + str(self.solver_properties['startTime']) + ';\n\n')
        self.file_manager.write(file_id, 'stopAt            endTime;\n\n')
        self.file_manager.write(file_id, 'endTime           ' + str(self.solver_properties['endTime']) + ';\n\n')
        self.file_manager.write(file_id, 'deltaT            ' + str(self.solver_properties['deltaT']) + ';\n\n')
        self.file_manager.write(file_id, 'maxDeltaT         ' + str(self.solver_properties['maxDeltaT']) + ';\n\n')
        if self.solver_properties['CFLBasedTimeStepping']:
            self.file_manager.write(file_id, 'adjustTimeStep    yes;\n\n')
        else:
            self.file_manager.write(file_id, 'adjustTimeStep    no;\n\n')
        self.file_manager.write(file_id, 'maxCo             ' + str(self.solver_properties['CFL']) + ';\n\n')
        if self.solver_properties['write_control'] == Parameters.TIME_STEP:
            self.file_manager.write(file_id, 'writeControl      timeStep;\n\n')
        elif self.solver_properties['write_control'] == Parameters.RUN_TIME:
            self.file_manager.write(file_id, 'writeControl      runTime;\n\n')
        elif self.solver_properties['write_control'] == Parameters.ADJUSTABLE_RUN_TIME:
            self.file_manager.write(file_id, 'writeControl      adjustableRunTime;\n\n')
        elif self.solver_properties['write_control'] == Parameters.CPU_TIME:
            self.file_manager.write(file_id, 'writeControl      cpuTime;\n\n')
        elif self.solver_properties['write_control'] == Parameters.CLOCK_TIME:
            self.file_manager.write(file_id, 'writeControl      clockTime;\n\n')
        self.file_manager.write(file_id, 'writeInterval     ' +
                                str(self.solver_properties['write_frequency']) + ';\n\n')
        self.file_manager.write(file_id, 'purgeWrite        ' + str(self.solver_properties['purge_write']) + ';\n\n')
        self.file_manager.write(file_id, 'writeFormat       ascii;\n\n')
        self.file_manager.write(file_id, 'writePrecision    6;\n\n')
        self.file_manager.write(file_id, 'writeCompression  off;\n\n')
        self.file_manager.write(file_id, 'timeFormat        general;\n\n')
        self.file_manager.write(file_id, 'timePrecision     6;\n\n')
        self.file_manager.write(file_id, 'runTimeModifiable true;\n\n')
        self.file_manager.write(file_id, 'functions\n')
        self.file_manager.write(file_id, '{\n')
        if self.solver_properties['write_force_coefficients']:
            self.file_manager.write(file_id, '    #include "forceCoefficients"\n')
        if self.solver_properties['turbulence_type']:
            self.file_manager.write(file_id, '    #include "yPlus"\n')
        self.file_manager.write(file_id, '    #include "residuals"\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
