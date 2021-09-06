import input.CaseProperties as CaseProperties
from input import GlobalVariables as Parameters

import src.FileDirectoryIO as FileIO
import src.Checker as Checker
import src.WriteSystemDirectoryFiles as SystemDir
import src.WriteConstantDirectoryFiles as ConstantDir
import src.WriteZeroDirectoryFiles as ZeroDir


def main():
    # process command line arguments first
    command_line_arguments = Checker.CheckCommandLineArguments()

    # get case specific dictionaries to set up case and write input files
    case_properties_handler = CaseProperties.CaseProperties()
    properties = case_properties_handler.get_case_properties(command_line_arguments)

    # check case (make sure that current set up will not produce any problem)
    check_case = Checker.CheckCase(properties)
    check_case.run_all_checks()

    # create the initial data structure for the case set-up
    file_manager = FileIO.FileManager(properties)
    file_manager.create_directory_structure()
    file_manager.copy_mesh_to_destination()

    # write out boundary conditions for all relevant flow properties
    boundary_conditions = ZeroDir.WriteBoundaryConditions(properties, file_manager)
    boundary_conditions.write_all_boundary_conditions()

    # write transport or thermo-physical properties depending on flow type
    if properties['flow_properties']['flow_type'] == Parameters.incompressible:
        transport_dict = ConstantDir.TransportPropertiesFile(properties, file_manager)
        transport_dict.write_input_file()
    elif properties['flow_properties']['flow_type'] == Parameters.compressible:
        thermo_dict = ConstantDir.ThermophysicalProperties(properties, file_manager)
        thermo_dict.write_input_file()

    # write turbulence properties to file
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(properties, file_manager)
    turbulence_dict.write_input_file()

    # write control dict file out
    control_dict = SystemDir.ControlDictFile(properties, file_manager)
    control_dict.write_input_file()

    # write fvSolution file out
    fv_solution = SystemDir.fvSolutionFile(properties, file_manager)
    fv_solution.write_input_file()

    # write fvSchemes
    fv_schemes = SystemDir.fvSchemesFile(properties, file_manager)
    fv_schemes.write_input_file()

    # write additional files if required for on-the-fly post-processing
    if properties['dimensionless_coefficients']['write_force_coefficients']:
        force_coefficients = SystemDir.WriteForceCoefficients(properties, file_manager)
        force_coefficients.write_force_coefficients()

    if Parameters.NONE not in properties['convergence_control']['integral_convergence_criterion']:
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
        decompose_par_dict = SystemDir.WriteDecomposeParDictionary(properties, file_manager)
        decompose_par_dict.write_decompose_par_dict()

    y_plus = SystemDir.WriteYPlus(properties, file_manager)
    y_plus.write_y_plus()

    residuals = SystemDir.WriteResiduals(file_manager)
    residuals.write_residuals()

    if properties['flow_properties']['flow_type'] == Parameters.compressible:
        mach_number = SystemDir.WriteMachNumber(properties, file_manager)
        mach_number.write_mach_number()

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
    screen_output.print_summary()


if __name__ == '__main__':
    main()
