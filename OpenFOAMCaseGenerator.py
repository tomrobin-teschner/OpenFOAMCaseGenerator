import src.CaseGenerator.Properties.CaseProperties as CaseProperties
from src.CaseGenerator.Properties.GlobalVariables import *

import src.CaseGenerator.FileDirectoryIO as FileIO
import src.CaseGenerator.Checker as Checker
import src.CaseGenerator.WriteSystemDirectoryFiles as SystemDir
import src.CaseGenerator.WriteConstantDirectoryFiles as ConstantDir
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir


def main():
    # process command line arguments first
    command_line_arguments = Checker.CheckCommandLineArguments()

    # get case specific dictionaries to set up case and write input files
    case_properties_handler = CaseProperties.CaseProperties(command_line_arguments)
    properties = case_properties_handler.get_case_properties()

    # check case (make sure that current set up will not produce any problem)
    check_case = Checker.CheckCase(properties)
    check_case.run_all_checks()

    # create the initial data structure for the case set-up
    file_manager = FileIO.FileManager(properties)
    file_manager.create_directory_structure()
    file_manager.copy_mesh_to_destination()

    boundary_conditions = ZeroDir.BoundaryConditionManager(properties)
    [variables, bcs] = boundary_conditions.get_all_boundary_conditions()
    for variable, bc in zip(variables, bcs):
        file_manager.write_content_to_file('0', variable, bc)

    # write transport or thermo-physical properties depending on flow type
    if properties['flow_properties']['flow_type'] == FlowType.incompressible:
        transport_dict = ConstantDir.TransportPropertiesFile(properties)
        file_manager.write_content_to_file('constant', 'transportProperties', transport_dict.get_file_content())
    elif properties['flow_properties']['flow_type'] == FlowType.compressible:
        thermo_dict = ConstantDir.ThermophysicalProperties(properties)
        file_manager.write_content_to_file('constant', 'thermophysicalProperties', thermo_dict.get_file_content())

    # write turbulence properties to file
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(properties)
    file_manager.write_content_to_file('constant', 'turbulenceProperties', turbulence_dict.get_file_content())

    # write control dict file out
    control_dict = SystemDir.ControlDictFile(properties)
    file_manager.write_content_to_file('system', 'controlDict', control_dict.get_file_content())
    if properties['post_processing']['execute_function_object']:
        fo_dict = properties['post_processing']['function_objects']
        for key, value in fo_dict.items():
            file_manager.write_content_to_file('system/include', key, control_dict.get_function_objects(key, value))

    # write fvSolution file out
    fv_solution = SystemDir.fvSolutionFile(properties)
    file_manager.write_content_to_file('system', 'fvSolution', fv_solution.get_file_content())

    # write fvSchemes
    fv_schemes = SystemDir.fvSchemesFile(properties)
    file_manager.write_content_to_file('system', 'fvSchemes', fv_schemes.get_file_content())

    # write additional files if required for on-the-fly post-processing
    if properties['dimensionless_coefficients']['write_force_coefficients']:
        force_coefficients = SystemDir.WriteForceCoefficients(properties, file_manager)
        force_coefficients.write_force_coefficients()

    if len(properties['convergence_control']['integral_convergence_criterion']) > 0:
        force_coefficient_trigger = SystemDir.WriteForceCoefficientConvergence(properties, file_manager)
        force_coefficient_trigger.write_triggers()

    if properties['dimensionless_coefficients']['write_pressure_coefficient']:
        pressure_coefficient = SystemDir.WritePressureCoefficient(properties, file_manager)
        pressure_coefficient.write_force_coefficients()

    if properties['point_probes']['write_point_probes']:
        point_probes = SystemDir.WritePointProbes(properties, file_manager)
        point_probes.write_point_probes()

    if properties['line_probes']['write_line_probes']:
        line_probes = SystemDir.WriteLineProbes(properties, file_manager)
        line_probes.write_line_probes()

    if properties['cutting_planes']['write_cutting_planes']:
        cutting_planes = SystemDir.WriteCuttingPlanes(properties, file_manager)
        cutting_planes.write_cutting_planes()

    if properties['iso_surfaces']['write_iso_surfaces']:
        iso_surfaces = SystemDir.WriteIsoSurfaces(properties, file_manager)
        iso_surfaces.write_iso_surfaces()

    if properties['additional_fields']['write_additional_fields'] or properties['iso_surfaces']['write_iso_surfaces']:
        fields = SystemDir.WriteFields(properties, file_manager)
        fields.write_field()

    if properties['parallel_properties']['run_in_parallel']:
        decompose_par_dict = SystemDir.WriteDecomposeParDictionary(properties)
        file_manager.write_content_to_file('system', 'decomposeParDict', decompose_par_dict.get_decompose_par_dict())

    y_plus = SystemDir.WriteYPlus(properties, file_manager)
    y_plus.write_y_plus()

    residuals = SystemDir.WriteResiduals(file_manager)
    residuals.write_residuals()

    if properties['flow_properties']['flow_type'] == FlowType.compressible:
        mach_number = SystemDir.WriteMachNumber(properties, file_manager)
        mach_number.write_mach_number()

    if ((properties['file_properties']['mesh_treatment'] == Mesh.snappy_hex_mesh_dict) and
            (len(properties['file_properties']['snappyhexmeshdict']['geometry']) > 0)):
        surface_features = SystemDir.WriteSurfaceFeatureExtract(properties, file_manager)
        surface_features.write_surface_feature_extract()

    # generate utility script class that produces useful scripts to run the simulation
    utility_scripts = FileIO.WriteUtilityScripts(properties, file_manager)

    # write Allrun file to execute case automatically
    utility_scripts.write_all_run_file()

    # write Allclean file to clean up case directory
    utility_scripts.write_all_clean_file()

    # copy residual plotting script over to case directory
    utility_scripts.copy_residual_plotting_script()

    # output diagnostics
    screen_output = FileIO.ScreenOutput(properties)
    screen_output.print_summary(command_line_arguments)


if __name__ == '__main__':
    main()
