import os, sys, warnings
from math import sqrt, pow

import FileDirectoryIO.FileManager as IO
import FileDirectoryIO.WriteUtilityScripts as UtilityScripts
import CheckCase.CheckCase as CheckCase
import WriteSystemDirectoryFiles.WriteForceCoefficients as ForceCoefficients
import WriteSystemDirectoryFiles.WritePressureCoefficient as PressureCoefficient
import WriteSystemDirectoryFiles.WriteDecomposePar as DecomposeParDict
import WriteSystemDirectoryFiles.WriteYPlus as YPlus
import WriteSystemDirectoryFiles.WriteResiduals as Residuals
import GlobalVariables as Parameters

import WriteConstantDirectoryFiles.WriteTransportProperties as Transport
import WriteConstantDirectoryFiles.WriteTurbulenceProperties as Turbulence
import WriteSystemDirectoryFiles.WriteControlDictFile as ControlDict
import WriteSystemDirectoryFiles.WritefvSolutionFile as fvSolution
import WriteSystemDirectoryFiles.WritefvSchemesFile as fvSchemes
import Write0DirectoryFiles.WriteBoundaryConditions as BoundaryConditions


def case_properties():
    file_properties = {
        # name of the case to use (will be used for the folder name)
        'case_name': 'naca_0012_y+_1',

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

        # freestream turbulent intensity (between 0 - 1)
        'freestream_turbulent_intensity': 0.00052,

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
        #   incompressible:
        #     simpleFoam: steady state, turbulent (RANS, LES) solver based on the SIMPLE algorithm
        #     icoFoam:    unsteady, non-turbulent (only laminar) solver based on the PISO algorithm
        #     pisoFoam:   unsteady, turbulent (RANS, LES) solver based on the PISO algorithm
        #     pimpleFoam: unsteady, turbulent (RANS, LES) solver based on the SIMPLE + PISO algorithm. May use higher
        #                 CFL numbers than pisoFoam while being more stable at the same time. Recommended in general
        'solver': Parameters.pimpleFoam,

        # start time
        'startTime': 0,

        # end time
        'endTime': 1000,

        # specify from which time directory to start from
        #   START_TIME:  Start from the folder that is defined in the startTime variable
        #   FIRST_TIME:  Start from the first available (lowest time) directory
        #   LATEST_TIME: Start from the latest available (highest time) directory. Use to restart a simulation from the
        #                last calculated solution
        'startFrom': Parameters.START_TIME,

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
        'write_frequency': 100,

        # write control, specify when to output results, the options are listed below
        #   TIME_STEP:           write every 'write_frequency' time steps
        #   RUN_TIME:            write data every 'write_frequency' seconds of simulated time
        #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
        #                        (use with 'CFLBasedTimeStepping' = True)
        #   CPU_TIME:            write data every 'write_frequency' seconds of CPU time
        #   CLOCK_TIME:          write data every 'write_frequency' seconds of real time
        'write_control': Parameters.TIME_STEP,

        # specify how many solutions to keep (specify 0 to keep all)
        'purge_write': 0,

        # time integration scheme, options are listed below
        #   STEADY_STATE: Do not integrate in time, i.e. dU / dt = 0
        #   UNSTEADY:     Integrate in time and resolve  dU / dt
        'time_integration': Parameters.STEADY_STATE,

        # Choose preset of numerical schemes based on accuracy and robustness requirements
        #   DEFAULT:    Optimal trade-off between accuracy and stability. Recommended for most cases. Tries to achieve
        #               second-order accuracy.
        #   TVD:        Same as DEFAULT, but use Total Variation Diminishing (TVD) schemes instead of upwind schemes.
        #   ROBUSTNESS: Use this option if your simulation does not converge or your mesh has bad mesh quality metrics.
        #               First-order accurate in space and time.
        #   ACCURACY:   Recommended for accuracy and scale resolved simulations (LES, DES, SAS). May be used after
        #               running a simulation with DEFAULT or ROBUSTNESS to increase accuracy. Second-order accurate with
        #               less limiting compared to DEFAULT and TVD.
        'numerical_schemes_correction': Parameters.ACCURACY,

        # flag to indicate if first order discretisation should be used for turbulent quantities
        'use_first_order_for_turbulence': True,

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

        # under-relaxation factor for Reynolds stresses
        'under_relaxation_reynolds_stresses': 0.5,

        # write force coefficients flag
        'write_force_coefficients': True,

        # write pressure coefficient (cp)
        'write_pressure_coefficient': True,
    }

    turbulence_properties = {
        # turbulence treatment type
        #   LAMINAR: Use this to run simulations without turbulence model (laminar or DNS)
        #   LES:     Use this for scale resolved simulations (LES, DES, SAS)
        #   RANS:    Use this for scale modelled / averaged simulations (RANS)
        'turbulence_type': Parameters.LES,

        # RANS turbulence model (will be ignored if turbulence_type != RANS)
        #   Based on linear eddy viscosity:
        #     kEpsilon:        standard k-epsilon model
        #     realizableKE:    realizable version of the k-epsilon model
        #     RNGkEpsilon:     renormalised group version of the k-epsilon model
        #     LienLeschziner:  Lien-Leschziner k-epsilon model (incompressible only)
        #     LamBremhorstKE:  Lam-Bremhorst k-epsilon model
        #     LaunderSharmaKE: Launder-Sharma k-epsilon model
        #
        #     kOmega:          standard k-omega model
        #     kOmegaSST:       standard k-omega SST model
        #
        #     qZeta:           q-zeta model (incompressible only, no wall functions)
        #
        #     SpalartAllmaras: standard Spalart-Allmaras model
        #
        #   Transition modelling
        #     kOmegaSSTLM:     gamma-Re,theta,t k-omega SST correlation-based transition model
        #     kkLOmega:        k_laminar, k_turbulent, omega physics-based transition model
        #
        #   Based on non-linear eddy viscosity:
        #     LienCubicKE:     Lien's k-epsilon model (incompressible only)
        #     ShihQuadraticKE: Shih's k-epsilon model (incompressible only)
        #
        #   Based on Reynolds Stresses
        #     LRR:             Reynolds stress model of Launder, Reece and Rodi
        #     SSG:             Reynolds stress model of Speziale, Sarkar and Gatski
        'turbulence_model': Parameters.kOmegaSST,

        # for RANS only, describe fidelity of wall modelling (i.e. usage of wall functions)
        #   LOW_RE  : first cell-height near wall is of order y+ <= 1
        #   HIGH_RE : first cell-height near wall is of order y+ >  30
        'wall_modelling': Parameters.LOW_RE,

        # select how to calculate turbulent quantities at inlet
        #   INTERNAL:    Internal flow assumes the turbulent length scale to be limited by the channel / wind tunnel
        #                height or diameter, expressed through the reference_length parameter. It is calculated as
        #                0.07 * reference length
        #   EXTERNAL:    External flow assumes the turbulent length scale to be limited by the scales within the
        #                fully turbulent boundary layer and approximately equal to 40% of the boundary layer thickness
        #   RATIO:       Alternatively, the turbulent to laminar viscosity ratio may be prescribed
        #   RATIO_AUTO:  In absence of any turbulent quantities, we may instead base the approximation of the turbulent
        #                to laminar viscosity ratio entirely on the freestream turbulence intensity. Use this option if
        #                any of the above are not suitable
        'turbulent_quantities_at_inlet': Parameters.EXTERNAL,

        # turbulent to laminar viscosity ratio. Only used when turbulent_quantities_at_inlet is set to RATIO
        'turbulent_to_laminar_ratio': 10,

        # do not overwrite setting here, used to set up numerical schemes correctly, depending on turbulence model
        # will get adjusted in main function
        'use_phi_instead_of_grad_U': False,
    }

    parallel_properties = {
        # flag indicating if simulation will be run in parallel. If true, additional information for domain
        # decomposition will be written (and Allrun script modified, accordingly)
        'run_in_parallel': False,

        # number of processors that will be used to run case in parallel
        'number_of_processors': 4,
    }

    return [file_properties, boundary_properties, flow_properties, solver_properties, turbulence_properties,
            parallel_properties]

def main():
    # get case specific dictionaries to set up case and write input files
    file_properties, boundary_properties, flow_properties, solver_properties, turbulence_properties, \
        parallel_properties = case_properties()

    # check case (make sure that current set up will not produce any problem)
    check_case = CheckCase.CheckCase(boundary_properties, solver_properties, turbulence_properties)
    check_case.check_correct_turbulence_model_setup()
    check_case.check_correct_boundary_condition_setup()
    check_case.check_appropriate_numerical_scheme_combination()

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

    # correct use_phi_instead_of_grad_U entry based on current turbulence model
    if (turbulence_properties['turbulence_model'] == Parameters.LienCubicKE or
            turbulence_properties['turbulence_model'] == Parameters.ShihQuadraticKE or
            turbulence_properties['turbulence_model'] == Parameters.LRR or
            turbulence_properties['turbulence_model'] == Parameters.SSG):
        turbulence_properties['use_phi_instead_of_grad_U'] = True

    # create the initial data structure for the case set-up
    file_manager = IO.FileManager(file_properties)
    file_manager.create_directory_structure()

    # write out boundary conditions for all relevant flow properties
    boundary_conditions = BoundaryConditions.WriteBoundaryConditions(file_manager, boundary_properties, flow_properties,
                                                                     solver_properties, turbulence_properties)
    boundary_conditions.write_U()
    boundary_conditions.write_p()
    boundary_conditions.write_k()
    boundary_conditions.write_kt()
    boundary_conditions.write_kl()
    boundary_conditions.write_nut()
    boundary_conditions.write_omega()
    boundary_conditions.write_epsilon()
    boundary_conditions.write_nuTilda()
    boundary_conditions.write_ReThetat()
    boundary_conditions.write_gammaInt()
    boundary_conditions.write_R()

    # write transport properties to file
    transport_dict = Transport.TransportPropertiesFile(file_manager, flow_properties)
    transport_dict.write_input_file()

    # write turbulence properties to file
    turbulence_dict = Turbulence.TurbulencePropertiesFile(file_manager, turbulence_properties)
    turbulence_dict.write_input_file()

    # write control dict file out
    control_dict = ControlDict.ControlDictFile(file_manager, solver_properties)
    control_dict.write_input_file()

    # write fvSolution file out
    fv_solution = fvSolution.fvSolutionFile(file_manager, solver_properties)
    fv_solution.write_input_file()

    # write fvSchemes
    fv_schemes = fvSchemes.fvSchemesFile(file_manager, solver_properties, turbulence_properties)
    fv_schemes.write_input_file()

    # write additional files if required for on-the-fly post-processing
    if solver_properties['write_force_coefficients']:
        force_coefficients = ForceCoefficients.WriteForceCoefficients(file_manager, flow_properties)
        force_coefficients.write_force_coefficients()

    if solver_properties['write_pressure_coefficient']:
        pressure_coefficient = PressureCoefficient.WritePressureCoefficient(file_manager, flow_properties)
        pressure_coefficient.write_force_coefficients()

    if parallel_properties['run_in_parallel']:
        decompose_par_dict = DecomposeParDict.WriteDecomposeParDictionary(file_manager, parallel_properties)
        decompose_par_dict.write_decompose_par_dict()

    yplus = YPlus.WriteYPlus(file_manager, flow_properties)
    yplus.write_y_plus()

    residuals = Residuals.WriteResiduals(file_manager)
    residuals.write_residuals()

    # generate utility script class that produces useful scripts to run the simulation
    utility_scripts = UtilityScripts.WriteUtilityScripts(file_properties, file_manager, solver_properties,
                                                         parallel_properties)

    # write Allrun file to execute case automatically
    utility_scripts.write_all_run_file()

    # write Allclean file to clean up case directory
    utility_scripts.write_all_clean_file()

    # output diagnostics
    print('Generated case : ' + file_properties['path'])
    print('Reynolds number: ' + str(reynolds_number))


if __name__ == '__main__':
    main()
