from src.Properties import GlobalVariables as Parameters


class ControlDictFile:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_input_file(self):
        file_id = self.file_manager.create_file('system', 'controlDict')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'controlDict')
        self.file_manager.write(file_id, '\n')
        if self.properties['solver_properties']['solver'] == Parameters.simpleFoam:
            self.file_manager.write(file_id, 'application       simpleFoam;\n\n')
        elif self.properties['solver_properties']['solver'] == Parameters.icoFoam:
            self.file_manager.write(file_id, 'application       icoFoam;\n\n')
        elif self.properties['solver_properties']['solver'] == Parameters.pisoFoam:
            self.file_manager.write(file_id, 'application       pisoFoam;\n\n')
        elif self.properties['solver_properties']['solver'] == Parameters.pimpleFoam:
            self.file_manager.write(file_id, 'application       pimpleFoam;\n\n')
        if self.properties['solver_properties']['startFrom'] == Parameters.START_TIME:
            self.file_manager.write(file_id, 'startFrom         startTime;\n\n')
        elif self.properties['solver_properties']['startFrom'] == Parameters.FIRST_TIME:
            self.file_manager.write(file_id, 'startFrom         firstTime;\n\n')
        elif self.properties['solver_properties']['startFrom'] == Parameters.LATEST_TIME:
            self.file_manager.write(file_id, 'startFrom         latestTime;\n\n')
        self.file_manager.write(file_id,
                                'startTime         ' + str(self.properties['solver_properties']['startTime']) + ';\n\n')
        self.file_manager.write(file_id, 'stopAt            endTime;\n\n')
        self.file_manager.write(file_id,
                                'endTime           ' + str(self.properties['solver_properties']['endTime']) + ';\n\n')
        self.file_manager.write(file_id,
                                'deltaT            ' + str(self.properties['solver_properties']['deltaT']) + ';\n\n')
        self.file_manager.write(file_id,
                                'maxDeltaT         ' + str(self.properties['solver_properties']['maxDeltaT']) + ';\n\n')
        if self.properties['solver_properties']['CFLBasedTimeStepping']:
            self.file_manager.write(file_id, 'adjustTimeStep    yes;\n\n')
        else:
            self.file_manager.write(file_id, 'adjustTimeStep    no;\n\n')
        self.file_manager.write(file_id,
                                'maxCo             ' + str(self.properties['solver_properties']['CFL']) + ';\n\n')
        if self.properties['solver_properties']['write_control'] == Parameters.TIME_STEP:
            self.file_manager.write(file_id, 'writeControl      timeStep;\n\n')
        elif self.properties['solver_properties']['write_control'] == Parameters.RUN_TIME:
            self.file_manager.write(file_id, 'writeControl      runTime;\n\n')
        elif self.properties['solver_properties']['write_control'] == Parameters.ADJUSTABLE_RUN_TIME:
            self.file_manager.write(file_id, 'writeControl      adjustableRunTime;\n\n')
        elif self.properties['solver_properties']['write_control'] == Parameters.CPU_TIME:
            self.file_manager.write(file_id, 'writeControl      cpuTime;\n\n')
        elif self.properties['solver_properties']['write_control'] == Parameters.CLOCK_TIME:
            self.file_manager.write(file_id, 'writeControl      clockTime;\n\n')
        self.file_manager.write(file_id, 'writeInterval     ' +
                                str(self.properties['solver_properties']['write_frequency']) + ';\n\n')
        self.file_manager.write(file_id, 'purgeWrite        ' +
                                str(self.properties['solver_properties']['purge_write']) + ';\n\n')
        self.file_manager.write(file_id, 'writeFormat       ascii;\n\n')
        self.file_manager.write(file_id, 'writePrecision    6;\n\n')
        self.file_manager.write(file_id, 'writeCompression  off;\n\n')
        self.file_manager.write(file_id, 'timeFormat        general;\n\n')
        self.file_manager.write(file_id, 'timePrecision     6;\n\n')
        self.file_manager.write(file_id, 'runTimeModifiable true;\n\n')
        self.file_manager.write(file_id, 'functions\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['additional_fields']['write_additional_fields']:
            self.file_manager.write(file_id, '    #include "include/fields"\n')
        if self.properties['dimensionless_coefficients']['write_force_coefficients']:
            self.file_manager.write(file_id, '    #include "include/forceCoefficients"\n')
        if len(self.properties['convergence_control']['integral_convergence_criterion']) > 0:
            self.file_manager.write(file_id, '    #include "include/forceCoefficientTrigger"\n')
        if self.properties['dimensionless_coefficients']['write_pressure_coefficient']:
            self.file_manager.write(file_id, '    #include "include/pressureCoefficient"\n')
        if self.properties['point_probes']['write_point_probes']:
            self.file_manager.write(file_id, '    #include "include/pointProbes"\n')
        if self.properties['line_probes']['write_line_probes']:
            self.file_manager.write(file_id, '    #include "include/lineProbes"\n')
        if self.properties['cutting_planes']['write_cutting_planes']:
            self.file_manager.write(file_id, '    #include "include/cuttingPlanes"\n')
        self.file_manager.write(file_id, '    #include "include/yPlus"\n')
        self.file_manager.write(file_id, '    #include "include/residuals"\n')
        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.file_manager.write(file_id, '    #include "include/MachNo"\n')
        if self.properties['dimensionless_coefficients']['write_wall_shear_stresses']:
            self.file_manager.write(file_id, '    #includeFunc "wallShearStress"\n')
        if self.properties['post_processing']['execute_function_object']:
            fo_dict = self.properties['post_processing']['function_objects']
            for key, value in fo_dict.items():
                self.file_manager.write(file_id, '    #include "include/' + key + '"\n')
                fo_id = self.file_manager.create_file('system/include', key)
                self.file_manager.write_header(fo_id, 'dictionary', 'system', key)
                self.file_manager.write(fo_id, '\n')
                with open(value, 'r') as fo_to_copy:
                    for line in fo_to_copy:
                        self.file_manager.write(fo_id, line)

        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
