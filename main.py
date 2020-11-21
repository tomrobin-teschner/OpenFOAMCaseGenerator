import os
from math import sqrt, pow

import FileDirectoryIO.FileManager as IO
import FileDirectoryIO.WriteUtilityScripts as UtilityScripts
import FileDirectoryIO.WriteForceCoefficients as ForceCoefficients
import GlobalVariables as Parameters

import WriteConstantDirectoryFiles.WriteTransportProperties as Transport
import WriteConstantDirectoryFiles.WriteTurbulenceProperties as Turbulence
import WriteSystemDirectoryFiles.WriteControlDictFile as ControlDict
import WriteSystemDirectoryFiles.WritefvSolutionFile as fvSolution
import WriteSystemDirectoryFiles.WritefvSchemesFile as fvSchemes
import Write0DirectoryFiles.WriteBoundaryConditions as BoundaryConditions


def main():

    # file properties
    file_properties = {
        # name of the case to use (will be used for the folder name)
        'case_name': 'naca_0012_y+_1_NASA',

        # path to folder where to copy test case to
        'run_directory': 'D:\\z_dataSecurity\\ubuntu\\OpenFOAM\\run',
        # 'run_directory': 'C:\\Users\\e802985\\Documents\\openfoam\\run',
        # 'run_directory': '',

        # version of openfoam to use (does not have an influence on the case setup, but will be used in headers)
        'version': 'v2006',
    }

    # define boundary conditions
    #   first  entry: name of boundary condition (specified in mesh generator)
    #   second entry: type of boundary condition
    #
    #   The following types are supported
    #   INLET:            Standard inlet condition, dirichlet for velocity + turbulence, neumann for pressure
    #   FREESTREAM:       Specify freestream condition globally (can be inlet and outlet)
    #   OUTLET:           Standard outlet, fixed pressure and Neumann for velocity + turbulence (Reflective outlet)
    #   BACKFLOW_OUTLET:  Same as outlet, but allows for flow to re-enter the domain (backflow at outlet)
    #   ADVECTIVE_OUTLET: Quantities are forced / advected outside domain (Non-reflective outlet)
    #   WALL:             Standard wall condition (ensure that mesh has wall boundary assigned instead of patch)
    #   EMPTY:            Used for essentially 2D simulations on the symmetry plane
    #   SYMMETRY:         Symmetry plane condition, i.e. wall with slip condition (Neumann condition for all quantities)
    #   CYCLIC:           Use for periodic flows (mesh needs to have CYCLIC conditions defined)
    boundary_properties = {
        'inlet': Parameters.FREESTREAM,
        'outlet': Parameters.FREESTREAM,
        'upper': Parameters.WALL,
        'lower': Parameters.WALL,
        'top_symmetry': Parameters.FREESTREAM,
        'bottom_symmetry': Parameters.FREESTREAM,
        'BaseAndTop': Parameters.EMPTY,
    }

    # physical properties of solver set-up
    flow_properties = {
        # specify the inlet boundary condition (free stream velocity)
        'inlet_velocity': [6, 0, 0],

        # specify the laminar viscosity
        'nu': 1e-6,

        # intensity of turbulent kinetic energy (between 0 - 1)
        'TKE_intensity': 0.0052,

        # reference length in simulation
        'reference_length': 1.0,

        # --------------------------------------------------------------------------------------------------------------
        # the following entries are only used by the force coefficients. If forces are not calculated, ignore these.

        # reference area used to non-dimensionalise force coefficients
        'reference_area': 1.0,

        # direction of lift vector (normalised to unity)
        'lift_direction': [0, 1, 0],

        # direction of drag vector (normalised to unity)
        'drag_direction': [1, 0, 0],

        # direction of pitch axis for momentum coefficient (normalised to unity)
        'pitch_axis_direction': [0, 0, 1],

        # center of rotation for momentum coefficient
        'center_of_roation': [-0.25, 0, 0],

        # group of wall boundaries, which should be used to calculate force coefficients on (enter as list)
        'wall_boundaries': ['lower', 'upper']
        # --------------------------------------------------------------------------------------------------------------
    }

    solver_properties = {
        # name of solver to use for simulation
        'solver': 'simpleFoam',

        # start time
        'startTime': 0,

        # end time
        'endTime': 3000,

        # flag indicating whether to dynamically caculate time step based on CFL criterion
        'CFLBasedTimeStepping': False,

        # CFL number
        'CFL': 1.0,

        # time step to be used (will be ignored if CFL-based time steppng is chosen)
        # WARNING: solver needs to support adjustable deltaT calculation
        'deltaT': 1,

        # largest allowable time step
        'maxDeltaT': 1,

        # frequency at which to write output files. Behaviour controlled through write control entry below.
        'write_frequency': 10,

        # write control, specify when to output results, the options are listed below
        #   TIME_STEP: write every 'write_frequency' time steps
        #   RUN_TIME: write data every 'write_frequency' seconds of simulated time
        #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
        #                        (use with 'CFLBasedTimeStepping' = True)
        #   CPU_TIME: write data every 'write_frequency' seconds of CPU time
        #   CLOCK_TIME: write data every 'write_frequency' seconds of real time
        'write_control': Parameters.TIME_STEP,

        # specify how many solutions to keep (specify 0 to keep all)
        'purge_write': 0,

        # turbulence treatment type
        # options are: LAMINAR, RANS, LES
        'turbulence_type': Parameters.RANS,

        # for RANS only, describe fidelity of wall modelling (i.e. usage of wall functions)
        #   LOW_RE  : first cell-height near wall is of order y+ <= 1
        #   HIGH_RE : first cell-height near wall is of order y+ >  30
        'wall_modelling': Parameters.LOW_RE,

        # time integration scheme, options are listed below
        #   STEADY_STATE: Do not integrate in time, i.e. dU / dt = 0
        #   FIRST_ORDER: Implicit Euler (1st-order)
        #   SECOND_ORDER: Implicit backward Euler (2nd-order)
        'time_integration': Parameters.STEADY_STATE,

        # spatial interpolation scheme for convective fluxes
        #   FIRST_ORDER: Upwind (1st-order)
        #   SECOND_ORDER: Upwind with Gradient correction (2nd-order)
        #   THIRD_ORDER: MUSCL scheme (3rd-order)
        'convective_fluxes': Parameters.FIRST_ORDER,

        # spatial interpolation of turbulent quantities for convective fluxes
        #   FIRST_ORDER: Upwind (1st-order)
        #   SECOND_ORDER: Upwind with Gradient correction (2nd-order)
        #   THIRD_ORDER: MUSCL scheme (3rd-order)
        'turbulent_fluxes': Parameters.FIRST_ORDER,

        # Choose level of corrections to be applied to numerical schemes in order to control stability and accuracy.
        #   NO_CORRECTION: No correction to be applied, best for accuracy and regular (orthogonal / cartesian) meshes
        #   SLIGHT_CORRECTION: Apply some correction. Best for unstructured meshes
        #   MODERATE_CORRECTION: Apply even more correction. Best for cases with convergence problems
        #   FULL_CORRECTION: Full correction is applied, best for poor quality meshes. Will reduce accuracy of solution
        'numerical_schemes_correction': Parameters.SLIGHT_CORRECTION,

        # absolute convergence criterion for implicit solvers
        'absolute_convergence_criterion': 1e-8,

        # relative convergence criterion for implicit solvers
        'relative_convergence_criterion': 0.01,

        # convergence criterion for flow solution
        'convergence_threshold': 1e-6,

        # under-relaxation factor for pressure
        'under_relaxation_p': 0.5,

        # under-relaxation factor for velocity
        'under_relaxation_U': 0.9,

        # under-relaxation factor for turbulent quantities
        'under_relaxation_turbulence': 0.9,

        # write force coefficients flag
        'write_force_coefficients': True,
    }

    # ------------------------------------------------------------------------------------------------------------------
    # add additional entries to dictionaries

    # absolute path of text case location
    file_properties['path'] = os.path.join(file_properties['run_directory'], file_properties['case_name'])

    # velocity magnitude
    velocity_magnitude = (sqrt(pow(flow_properties['inlet_velocity'][0], 2) +
                               pow(flow_properties['inlet_velocity'][1], 2) +
                               pow(flow_properties['inlet_velocity'][2], 2)))
    flow_properties['velocity_magnitude'] = velocity_magnitude

    # Reynolds number calculation
    reynolds_number = (velocity_magnitude * flow_properties['reference_length'] / flow_properties['nu'])
    flow_properties['reynolds_number'] = reynolds_number

    # ------------------------------------------------------------------------------------------------------------------

    # create the initial data structure for the case set-up
    file_manager = IO.FileManager(file_properties)
    file_manager.create_directory_structure()

    # write out boundary conditions for all relevant flow properties
    boundary_conditions = BoundaryConditions.WriteBoundaryConditions(file_manager, boundary_properties, flow_properties,
                                                                     solver_properties)
    boundary_conditions.write_U()
    boundary_conditions.write_p()
    boundary_conditions.write_k()
    boundary_conditions.write_nut()
    boundary_conditions.write_omega()
    boundary_conditions.write_epsilon()
    boundary_conditions.write_nuTilda()
    boundary_conditions.write_ReThetat()
    boundary_conditions.write_gammaInt()
    boundary_conditions.write_R()

    # write transport properties to file
    transport_properties = Transport.TransportPropertiesFile(file_manager, flow_properties)
    transport_properties.write_input_file()

    # write turbulence properties to file
    turbulence_properties = Turbulence.TurbulencePropertiesFile(file_manager, solver_properties)
    turbulence_properties.write_input_file()

    # write control dict file out
    control_dict = ControlDict.ControlDictFile(file_manager, solver_properties)
    control_dict.write_input_file()

    # write fvSolution file out
    fv_solution = fvSolution.fvSolutionFile(file_manager, solver_properties)
    fv_solution.write_input_file()

    # write fvSchemes
    fv_schemes = fvSchemes.fvSchemesFile(file_manager, solver_properties)
    fv_schemes.write_input_file()

    # write additional files if required
    if solver_properties['write_force_coefficients']:
        force_coefficients = ForceCoefficients.WriteForceCoefficients(file_manager, flow_properties)
        force_coefficients.write_force_coefficients()

    # generate utility script class that produces useful scripts to run the simulation
    utility_scripts = UtilityScripts.WriteUtilityScripts(file_properties, file_manager, solver_properties)

    # write Allrun file to execute case automatically
    utility_scripts.write_all_run_file()

    # write Allclean file to clean up case directory
    utility_scripts.write_all_clean_file()

    # output diagnostics
    print('Generated case : ' + file_properties['path'])
    print('Reynolds number: ' + str(reynolds_number))


if __name__ == '__main__':
    main()