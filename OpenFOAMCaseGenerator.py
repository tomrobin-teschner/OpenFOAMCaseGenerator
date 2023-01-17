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
    properties = case_properties_handler.get_case()

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
        force_coefficients = SystemDir.ForceCoefficients(properties)
        file_manager.write_content_to_file('system/include', 'forceCoefficients', force_coefficients.get_file_content())

    if len(properties['convergence_control']['integral_convergence_criterion']) > 0:
        triggers = SystemDir.ForceCoefficientConvergence(properties)
        file_manager.write_content_to_file('system/include', 'forceCoefficientTrigger', triggers.get_file_content())

    if properties['dimensionless_coefficients']['write_pressure_coefficient']:
        cp_coefficients = SystemDir.PressureCoefficient(properties)
        file_manager.write_content_to_file('system/include', 'pressureCoefficient', cp_coefficients.get_file_content())

    if properties['point_probes']['write_point_probes']:
        point_probes = SystemDir.PointProbes(properties)
        file_manager.write_content_to_file('system/include', 'pointProbes', point_probes.get_file_content())

    if properties['line_probes']['write_line_probes']:
        line_probes = SystemDir.LineProbes(properties)
        file_manager.write_content_to_file('system/include', 'lineProbes', line_probes.get_file_content())

    if properties['cutting_planes']['write_cutting_planes']:
        cutting_planes = SystemDir.CuttingPlanes(properties)
        file_manager.write_content_to_file('system/include', 'cuttingPlanes', cutting_planes.get_file_content())

    if properties['iso_surfaces']['write_iso_surfaces']:
        iso_surfaces = SystemDir.IsoSurfaces(properties)
        file_manager.write_content_to_file('system/include', 'isoSurfaces', iso_surfaces.get_file_content())

    if properties['additional_fields']['write_additional_fields'] or properties['iso_surfaces']['write_iso_surfaces']:
        fields = SystemDir.AdditionalFields(properties)
        file_manager.write_content_to_file('system/include', 'fields', fields.get_file_content())

    if properties['parallel_properties']['run_in_parallel']:
        decompose_par_dict = SystemDir.DecomposeParDictionary(properties)
        file_manager.write_content_to_file('system', 'decomposeParDict', decompose_par_dict.get_decompose_par_dict())

    if properties['turbulence_properties']['turbulence_type'] is not TurbulenceType.laminar:
        y_plus = SystemDir.YPlus(properties)
        file_manager.write_content_to_file('system/include', 'yPlus', y_plus.get_file_content())

    residuals = SystemDir.Residuals(properties)
    file_manager.write_content_to_file('system/include', 'residuals', residuals.get_file_content())

    if properties['flow_properties']['flow_type'] == FlowType.compressible:
        mach_number = SystemDir.MachNumber(properties)
        file_manager.write_content_to_file('system/include', 'MachNo', mach_number.get_file_content())

    if ((properties['file_properties']['mesh_treatment'] == Mesh.snappy_hex_mesh_dict) and
            (len(properties['file_properties']['snappyhexmeshdict']['geometry']) > 0)):
        surface_features = SystemDir.SurfaceFeatureExtract(properties)
        file_manager.write_content_to_file('system', 'surfaceFeatureExtractDict', surface_features.get_file_content())

    # generate utility script class that produces useful scripts to run the simulation
    utility_scripts = FileIO.UtilityScripts(properties)

    # write Allrun file to execute case automatically
    file_manager.write_content_to_file('', 'Allrun', utility_scripts.get_all_run_content())

    # write Allclean file to clean up case directory
    file_manager.write_content_to_file('', 'Allclean', utility_scripts.get_all_clean_content())

    # copy residual plotting script over to case directory
    utility_scripts.copy_residual_plotting_script()

    # output diagnostics
    screen_output = FileIO.ScreenOutput(properties)
    screen_output.print_summary(command_line_arguments)


if __name__ == '__main__':
    main()
