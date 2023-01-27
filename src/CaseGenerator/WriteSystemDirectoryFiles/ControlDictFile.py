from os import path
from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator.FileDirectoryIO import WriteHeader

class ControlDictFile:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        control_dict = WriteHeader.get_header(version, 'dictionary', 'system', 'controlDict')

        time_discretisation = {}
        if self.properties['time_discretisation']['time_integration'] == TimeTreatment.steady_state:
            time_discretisation = self.properties['time_discretisation']['steady_state_properties']
        elif self.properties['time_discretisation']['time_integration'] == TimeTreatment.unsteady:
            time_discretisation = self.properties['time_discretisation']['unsteady_properties']

        control_dict += f'application       {self.properties["solver_properties"]["solver"].name};\n\n'
        if time_discretisation['startFrom'] == SimulationStart.startTime:
            control_dict += f'startFrom         startTime;\n\n'
        elif time_discretisation['startFrom'] == SimulationStart.firstTime:
            control_dict += f'startFrom         firstTime;\n\n'
        elif time_discretisation['startFrom'] == SimulationStart.latestTime:
            control_dict += f'startFrom         latestTime;\n\n'
        control_dict += f'startTime         {time_discretisation["startTime"]};\n\n'
        control_dict += f'stopAt            endTime;\n\n'
        control_dict += f'endTime           {time_discretisation["endTime"]};\n\n'
        control_dict += f'deltaT            {time_discretisation["deltaT"]};\n\n'
        control_dict += f'maxDeltaT         {time_discretisation["maxDeltaT"]};\n\n'
        if time_discretisation['CFLBasedTimeStepping']:
            control_dict += f'adjustTimeStep    yes;\n\n'
        else:
            control_dict += f'adjustTimeStep    no;\n\n'
        control_dict += f'maxCo             ' + str(time_discretisation['CFL']) + ';\n\n'
        if time_discretisation['write_control'] == OutputWriteControl.timeStep:
            control_dict += f'writeControl      timeStep;\n\n'
        elif time_discretisation['write_control'] == OutputWriteControl.runTime:
            control_dict += f'writeControl      runTime;\n\n'
        elif time_discretisation['write_control'] == OutputWriteControl.adjustableRunTime:
            control_dict += f'writeControl      adjustableRunTime;\n\n'
        elif time_discretisation['write_control'] == OutputWriteControl.cpuTime:
            control_dict += f'writeControl      cpuTime;\n\n'
        elif time_discretisation['write_control'] == OutputWriteControl.clockTime:
            control_dict += f'writeControl      clockTime;\n\n'
        control_dict += f'writeInterval     {time_discretisation["write_frequency"]};\n\n'
        control_dict += f'purgeWrite        {time_discretisation["purge_write"]};\n\n'
        control_dict += f'writeFormat       ascii;\n\n'
        control_dict += f'writePrecision    6;\n\n'
        control_dict += f'writeCompression  off;\n\n'
        control_dict += f'timeFormat        general;\n\n'
        control_dict += f'timePrecision     6;\n\n'
        control_dict += f'runTimeModifiable true;\n\n'
        control_dict += f'functions\n'
        control_dict += f'{{\n'
        if self.properties['additional_fields']['write_additional_fields']:
            control_dict += f'    #include "include/fields"\n'
        if self.properties['iso_surfaces']['write_iso_surfaces']:
            control_dict += f'    #include "include/isoSurfaces"\n'
        if self.properties['dimensionless_coefficients']['write_force_coefficients']:
            control_dict += f'    #include "include/forceCoefficients"\n'
        if len(self.properties['convergence_control']['integral_convergence_criterion']) > 0:
            control_dict += f'    #include "include/forceCoefficientTrigger"\n'
        if self.properties['dimensionless_coefficients']['write_pressure_coefficient']:
            control_dict += f'    #include "include/pressureCoefficient"\n'
        if self.properties['point_probes']['write_point_probes']:
            control_dict += f'    #include "include/pointProbes"\n'
        if self.properties['line_probes']['write_line_probes']:
            control_dict += f'    #include "include/lineProbes"\n'
        if self.properties['cutting_planes']['write_cutting_planes']:
            control_dict += f'    #include "include/cuttingPlanes"\n'
        if self.properties['turbulence_properties']['turbulence_type'] != TurbulenceType.laminar:
            control_dict += f'    #include "include/yPlus"\n'
        control_dict += f'    #include "include/residuals"\n'
        if self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            control_dict += f'    #include "include/MachNo"\n'
        if self.properties['dimensionless_coefficients']['write_wall_shear_stresses']:
            control_dict += f'    #includeFunc "wallShearStress"\n'
        if self.properties['post_processing']['execute_function_object']:
            fo_dict = self.properties['post_processing']['function_objects']
            for key in fo_dict.keys():
                control_dict += f'    #include "include/{key}"\n'
        control_dict += f'}}\n\n'
        control_dict += f'// ************************************************************************* //\n'
        return control_dict

    def get_function_objects(self, fo_name, file_location):
        version = self.properties['file_properties']['version']
        fo_string = WriteHeader.get_header(version, 'dictionary', 'system', fo_name)
        fo_to_copy_id = open(file_location, 'r')
        for line in fo_to_copy_id.readlines():
            fo_string += line
        fo_to_copy_id.close()
        return fo_string
