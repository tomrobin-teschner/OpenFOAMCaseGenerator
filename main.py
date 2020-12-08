import os
from math import sqrt, pow

import FileDirectoryIO.FileManager as IO
import FileDirectoryIO.WriteUtilityScripts as UtilityScripts
import CheckCase.CheckCase as CheckCase
import WriteSystemDirectoryFiles.WriteForceCoefficients as ForceCoefficients
import WriteSystemDirectoryFiles.WritePressureCoefficient as PressureCoefficient
import WriteSystemDirectoryFiles.WriteDecomposePar as DecomposeParDict
import WriteSystemDirectoryFiles.WriteYPlus as YPlus
import WriteSystemDirectoryFiles.WriteResiduals as Residuals
import WriteSystemDirectoryFiles.WriteForceCoefficientConvergence as ForceCoefficientTrigger
import WriteSystemDirectoryFiles.WritePointProbes as PointProbes
import WriteSystemDirectoryFiles.WriteLineProbes as LineProbes
import WriteSystemDirectoryFiles.WriteCuttingPlanes as CuttingPlanes
import WriteSystemDirectoryFiles.WriteFields as AdditionalFields
import WriteSystemDirectoryFiles.WriteIsoSurfaces as IsoSurfaces
import GlobalVariables as Parameters

import WriteConstantDirectoryFiles.WriteTransportProperties as Transport
import WriteConstantDirectoryFiles.WriteTurbulenceProperties as Turbulence
import WriteSystemDirectoryFiles.WriteControlDictFile as ControlDict
import WriteSystemDirectoryFiles.WritefvSolutionFile as fvSolution
import WriteSystemDirectoryFiles.WritefvSchemesFile as fvSchemes
import Write0DirectoryFiles.WriteBoundaryConditions as BoundaryConditions


def case_properties():
    properties = {
        'file_properties': {
            # name of the case to use (will be used for the folder name)
            'case_name': '',

            # path to where the currently generated case should be copied to (parent directory)
            # if left empty, the case will be written into the current directory
            'run_directory': '',

            # version of openfoam to use (does not have an influence on the case setup, but will be used in headers)
            'version': 'v2006',
        },

        # setting up simulation for parallel processing
        'parallel_properties': {
            # flag indicating if simulation will be run in parallel. If true, additional information for domain
            # decomposition will be written (and Allrun script modified, accordingly)
            'run_in_parallel': False,

            # number of processors that will be used to run case in parallel
            'number_of_processors': 4,
        },

        # define boundary conditions
        #   first  entry: name of boundary condition (specified in mesh generator)
        #   second entry: type of boundary condition (see below)
        #
        #   The following types are supported
        #   INLET:            Standard inlet condition, dirichlet for velocity + turbulence, neumann for pressure
        #   FREESTREAM:       Specify freestream condition globally (can be inlet and outlet)
        #   OUTLET:           Standard outlet, fixed pressure and Neumann for velocity + turbulence (Reflective outlet)
        #   BACKFLOW_OUTLET:  Same as outlet, but allows for flow to re-enter the domain (backflow at outlet)
        #   ADVECTIVE_OUTLET: Quantities are forced / advected outside domain (Non-reflective outlet)
        #   WALL:             Standard wall condition (ensure that mesh has wall boundary assigned instead of patch)
        #   EMPTY:            Used for essentially 2D simulations on the symmetry plane
        #   SYMMETRY:         Symmetry plane condition, i.e. wall with slip condition
        #                     (Neumann condition for all quantities)
        #   CYCLIC:           Use for periodic flows (mesh needs to have CYCLIC conditions defined)
        'boundary_properties': {
            'inlet': Parameters.INLET,
            'outlet': Parameters.OUTLET,
            'wall': Parameters.WALL,
            'leadingEdge': Parameters.WALL,
            'symmetry': Parameters.SYMMETRY,
            'BaseAndTop': Parameters.EMPTY,
        },

        # physical properties of solver set-up
        'flow_properties': {
            # specify the inlet boundary condition (free stream velocity)
            'inlet_velocity': [30, 0, 0],

            # set initial velocity field everywhere to inlet velocity?
            'initial_velocity_field_is_inlet_velocity': False,

            # specify the laminar viscosity
            'nu': 1.47e-5,

            # freestream turbulent intensity (between 0 - 1)
            'freestream_turbulent_intensity': 0.00051,

            # reference length in simulation
            'reference_length': 1.5,
        },

        'solver_properties': {
            # name of solver to use for simulation
            #   incompressible:
            #     simpleFoam: steady state, turbulent (RANS) solver based on the SIMPLE algorithm
            #     icoFoam:    unsteady, non-turbulent (only laminar) solver based on the PISO algorithm
            #     pisoFoam:   unsteady, turbulent (RANS, LES) solver based on the PISO algorithm
            #     pimpleFoam: unsteady, turbulent (RANS, LES) solver based on the SIMPLE + PISO algorithm. May use
            #                 higher CFL numbers than pisoFoam while being more stable. Recommended in general
            'solver': Parameters.simpleFoam,

            # start time
            'startTime': 0,

            # end time
            'endTime': 10000,

            # specify from which time directory to start from
            #   START_TIME:  Start from the folder that is defined in the startTime variable
            #   FIRST_TIME:  Start from the first available (lowest time) directory
            #   LATEST_TIME: Start from the latest available (highest time) directory. Use to restart a simulation from
            #                the last calculated solution
            'startFrom': Parameters.START_TIME,

            # flag indicating whether to dynamically calculate time step based on CFL criterion
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
            #   TIME_STEP:           write every 'write_frequency' time steps
            #   RUN_TIME:            write data every 'write_frequency' seconds of simulated time
            #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
            #                        (use with 'CFLBasedTimeStepping' = True)
            #   CPU_TIME:            write data every 'write_frequency' seconds of CPU time
            #   CLOCK_TIME:          write data every 'write_frequency' seconds of real time
            'write_control': Parameters.TIME_STEP,

            # specify how many solutions to keep (specify 0 to keep all)
            'purge_write': 0,

            # under-relaxation factor for pressure
            'under_relaxation_p': 0.1,

            # under-relaxation factor for velocity
            'under_relaxation_U': 0.1,

            # under-relaxation factor for turbulent quantities
            'under_relaxation_turbulence': 0.1,

            # under-relaxation factor for Reynolds stresses
            'under_relaxation_reynolds_stresses': 0.1,
        },

        'numerical_discretisation': {
            # time integration scheme, options are listed below
            #   STEADY_STATE: Do not integrate in time, i.e. dU / dt = 0
            #   UNSTEADY:     Integrate in time and resolve  dU / dt
            'time_integration': Parameters.STEADY_STATE,

            # Choose preset of numerical schemes based on accuracy and robustness requirements
            #   DEFAULT:    Optimal trade-off between accuracy and stability. Recommended for most cases. Tries to
            #               achieve second-order accuracy.
            #   TVD:        Same as DEFAULT, but use Total Variation Diminishing (TVD) schemes instead of upwind schemes
            #   ROBUSTNESS: Use this option if your simulation does not converge or your mesh has bad mesh quality
            #               metrics. First-order accurate in space and time
            #   ACCURACY:   Recommended for accuracy and scale resolved simulations (LES, DES, SAS). May be used after
            #               running a simulation with DEFAULT or ROBUSTNESS to increase accuracy. Second-order accurate
            #               with less limiting compared to DEFAULT and TVD.
            'numerical_schemes_correction': Parameters.ROBUSTNESS,

            # choose the amount of limiter to use. A high value may limit more strongly but can slow down convergence
            #

            # flag to indicate if first order discretisation should be used for turbulent quantities
            'use_first_order_for_turbulence': True,
        },

        'turbulence_properties': {
            # turbulence treatment type
            #   LAMINAR: Use this to run simulations without turbulence model (laminar or DNS)
            #   LES:     Use this for scale resolved simulations (LES, DES, SAS)
            #   RANS:    Use this for scale modelled / averaged simulations (RANS)
            'turbulence_type': Parameters.RANS,

            # for RANS only, describe fidelity of wall modelling (i.e. usage of wall functions)
            #   LOW_RE  : first cell-height near wall is of order y+ <= 1
            #   HIGH_RE : first cell-height near wall is of order y+ >  30
            'wall_modelling': Parameters.LOW_RE,

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
            #   Scale-Adaptive modelling
            #     kOmegaSSTSAS:    Scale-adaptive version of the k-omega SST model
            #
            #   Based on non-linear eddy viscosity:
            #     LienCubicKE:     Lien's k-epsilon model (incompressible only)
            #     ShihQuadraticKE: Shih's k-epsilon model (incompressible only)
            #
            #   Based on Reynolds Stresses
            #     LRR:             Reynolds stress model of Launder, Reece and Rodi
            #     SSG:             Reynolds stress model of Speziale, Sarkar and Gatski
            'RANS_model': Parameters.kOmegaSST,

            # LES / DES model
            #   LES:
            #     Smagorinsky:         Large Eddy Simulation based on classical Smagorinsky approach (fixed C_s)
            #     kEqn:                solve transport equation for sub-grid scale kinetic energy k_sgs
            #     dynamicKEqn:
            #     dynamicLagrangian:
            #     DeardorffDiffStress:
            #     WALE:                Wall adapting local eddy (WALE)
            #
            #   DES:
            #     SpalartAllmarasDES:   Detached Eddy Simulation based on the Spalart-Allmaras model
            #     SpalartAllmarasDDES:  Delayed Detached Eddy Simulation based on the Spalart-llmaras model
            #     SpalartAllmarasIDDES: Improved Delayed Detached Eddy Simulation based on the Spalart-Allmaras model
            #     kOmegaSSTDES:         Detached Eddy Simulation based on the k-omega SST model
            #     kOmegaSSTDDES:        Delayed Detached Eddy Simulation based on the k-omega SST model
            #     kOmegaSSTIDDES:       Improved Delayed Detached Eddy Simulation based on the k-omega SST model
            'LES_model': Parameters.Smagorinsky,

            # model to calculate delta coefficient in LES / DES model
            #   smooth:
            #   Prandtl:
            #   maxDeltaxyz:
            #   cubeRootVol:         Take the cube root of the volume as delta
            #   maxDeltaxyzCubeRoot:
            #   vanDriest:           Applies van Driest damping function close to the wall
            #   IDDESDelta:
            'delta_model': Parameters.cubeRootVol,

            # select how to calculate turbulent quantities at inlet
            #   INTERNAL:    Internal flow assumes the turbulent length scale to be limited by the channel / wind tunnel
            #                height or diameter, expressed through the reference_length parameter. It is calculated as
            #                0.07 * reference length
            #   EXTERNAL:    External flow assumes the turbulent length scale to be limited by the scales within the
            #                fully turbulent boundary layer and approximately equal to 40% of the boundary layer
            #                thickness
            #   RATIO:       Alternatively, the turbulent to laminar viscosity ratio may be prescribed
            #   RATIO_AUTO:  In absence of any turbulent quantities, we may instead base the approximation of the
            #                turbulent to laminar viscosity ratio entirely on the freestream turbulence intensity.
            #                Use this option if any of the above are not suitable
            'turbulent_quantities_at_inlet': Parameters.EXTERNAL,

            # turbulent to laminar viscosity ratio. Only used when turbulent_quantities_at_inlet is set to RATIO
            'turbulent_to_laminar_ratio': 10,
        },

        'convergence_control': {
            # convergence criterion for residuals (used to judge if a simulation has converged)
            'convergence_threshold': 1e-5,

            # absolute convergence criterion for implicit solvers (used to judge if the current iteration has converged)
            'absolute_convergence_criterion': 1e-8,

            # relative convergence criterion for implicit solvers (used to judge if the current iteration has converged)
            'relative_convergence_criterion': 0.01,

            # check if an integral quantity has converged instead of just checking the residuals
            # recommended if such a integral quantity can be easily defined for the current simulation
            #   NONE:                 Don't write any force coefficient based stopping criterion
            #   C_D:                  Convergence criterion based on the drag force coefficient
            #   C_L:                  Convergence criterion based on the lift force coefficient
            #   C_S:                  Convergence criterion based on the side force coefficient
            #   C_M_YAW:              Convergence criterion based on the yaw momentum coefficient
            #   C_M_ROLL:             Convergence criterion based on the roll momentum coefficient
            #   C_M_PITCH:            Convergence criterion based on the pitch momentum coefficient
            'integral_convergence_criterion': Parameters.NONE,

            # if integral quantities are checked for convergence, specify for how many timesteps their average should be
            # calculated to check if, on average, the quantity has converged
            'averaging_time_steps': 20,

            # specify the convergence threshold for the integral quantities
            'integral_quantities_convergence_threshold': 1e-4,

            # specify how many iterations to wait before checking convergence criterion
            'time_steps_to_wait_before_checking_convergence': 100,
        },

        'dimensionless_coefficients': {
            # reference area used to non-dimensionalise force coefficients
            'reference_area': 3.78378e-3,

            # direction of lift vector (normalised to unity)
            'lift_direction': [0, 1, 0],

            # direction of drag vector (normalised to unity)
            'drag_direction': [1, 0, 0],

            # direction of pitch axis for momentum coefficient (normalised to unity)
            'pitch_axis_direction': [0, 0, 1],

            # center of rotation for momentum coefficient
            'center_of_roation': [0, 0, 0],

            # group of wall boundaries, which should be used to calculate force coefficients on (enter as list)
            'wall_boundaries': ['wall', 'leadingEdge'],

            # write force coefficients flag
            'write_force_coefficients': True,

            # write pressure coefficient (cp)
            'write_pressure_coefficient': False,

            # write wall shear stresses (can be used to obtain skin friction coefficient)
            'write_wall_shear_stresses': False,
        },

        # write out additional fields of interest
        'additional_fields': {
            # list of additional fields to write, can be more than 1
            #   Q:         Write out the Q-criterion, useful for isoSurfaces to visualise turbulence structures
            #   VORTICITY: Write out vorticity field
            #   LAMBDA_2:  Write out the Lambda-2 criterion, useful for vortex core detection
            #   ENSTROPHY: Write out enstrophy field (useful for turbulent studies)
            'fields': [Parameters.Q],

            # flag indicating if additional fields should be active (written to file). Will be written with all other
            # variables to file at the same time.
            'write_additional_fields': False,
        },

        # specify 0-D point probes to which will output flow variables at each timestep at a given location x, y and z
        'point_probes': {
            # specify the location at which to output information, can be more than 1
            'location': [
                [1, 0.01, 0],
                [2, 0, 0],
            ],

            # specify variables that should be monitored at the specified point
            'variables_to_monitor': ['U', 'p'],

            # flag indicating if point probes should be active (written to file)
            'write_point_probes': False,

            # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only be
            # written according to the settings in the controlDict (i.e. every time a new time directory is generated)
            'output_probe_at_every_timestep': True,
        },

        # specify 1-D line probes
        'line_probes': {
            # specify the start and end point where line should be placed, can be more than 1
            'location': [
                {
                    'name': 'x=2',
                    'start': [2, 1, 0.5],
                    'end': [2, -1, 0.5],
                },
                {
                    'name': 'x=5',
                    'start': [5, 1, 0.5],
                    'end': [5, -1, 0.5],
                },
            ],

            # number of points along line
            'number_of_samples_on_line': 100,

            # specify variables that should be monitored along line
            'variables_to_monitor': ['U', 'p'],

            # flag indicating if point probes should be active (written to file)
            'write_line_probes': False,

            # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only be
            # written according to the settings in the controlDict (i.e. every time a new time directory is generated)
            'output_probe_at_every_timestep': False,
        },

        # specify 2-D cutting planes
        'cutting_planes': {
            # specify the origin and normal vector of cutting plane, can be more than 1
            'location': [
                {
                    'name': 'plane_z=5',
                    'origin': [0, 0, 0.5],
                    'normal': [0, 0, 1],
                },
                {
                    'name': 'plane_y=5',
                    'origin': [-1, 0, 0.5],
                    'normal': [0, 1, 0],
                },
            ],

            # specify variables that should be monitored along line
            'variables_to_monitor': ['U', 'p'],

            # flag indicating if point probes should be active (written to file)
            'write_cutting_planes': False,

            # if flag is set to true, solution will be written at every time step. Otherwise, the cutting plane will
            # only be written according to the settings in the controlDict (i.e. every time a new time directory is
            # generated)
            'output_cutting_plane_at_every_timestep': False,
        },

        # write iso surfaces of variables during calculation
        'iso_surfaces': {
            # variables of which to write iso surfaces
            'flow_variable': ['Q', 'Lambda2'],

            # iso value at which point the surface should be written. List entry correspond to order specified in
            # flow_variable list
            'iso_value': [1e-5, 0],

            # additional fields to write (can be more than 1, can be used to colour iso-surface in post-processing)
            'additional_field_to_write': ['p'],

            # flag indicating if iso-surfaces should be active (written to file)
            'write_iso_surfaces': False,

            # if flag is set to true, iso-surfaces will be written at every time step. Otherwise, the iso surfaces will
            # only be written according to the settings in the controlDict (i.e. every time a new time directory is
            # generated)
            'output_iso_surfaces_at_every_timestep': False,
        },
    }

    return properties


def add_default_properties(properties):
    # absolute path of text case location
    properties['file_properties']['path'] = \
        os.path.join(properties['file_properties']['run_directory'], properties['file_properties']['case_name'])

    # velocity magnitude
    velocity_magnitude = (sqrt(pow(properties['flow_properties']['inlet_velocity'][0], 2) +
                               pow(properties['flow_properties']['inlet_velocity'][1], 2) +
                               pow(properties['flow_properties']['inlet_velocity'][2], 2)))
    properties['flow_properties']['velocity_magnitude'] = velocity_magnitude

    # Reynolds number calculation
    reynolds_number = (velocity_magnitude * properties['flow_properties']['reference_length'] /
                       properties['flow_properties']['nu'])
    properties['flow_properties']['reynolds_number'] = reynolds_number

    # some turbulence models require phi instead of grad(U) in their discretisation, set this up automatically here
    properties['turbulence_properties']['use_phi_instead_of_grad_U'] = False,
    if (properties['turbulence_properties']['RANS_model'] == Parameters.LienCubicKE or
            properties['turbulence_properties']['RANS_model'] == Parameters.ShihQuadraticKE or
            properties['turbulence_properties']['RANS_model'] == Parameters.LRR or
            properties['turbulence_properties']['RANS_model'] == Parameters.SSG):
        properties['turbulence_properties']['use_phi_instead_of_grad_U'] = True

    return properties


def main():
    # get case specific dictionaries to set up case and write input files
    properties = case_properties()

    # check case (make sure that current set up will not produce any problem)
    check_case = CheckCase.CheckCase(properties)
    check_case.check_correct_turbulence_model_setup()
    check_case.check_correct_boundary_condition_setup()
    check_case.check_appropriate_numerical_scheme_combination()

    # add additional entries to dictionaries
    add_default_properties(properties)

    # create the initial data structure for the case set-up
    file_manager = IO.FileManager(properties)
    file_manager.create_directory_structure()

    # write out boundary conditions for all relevant flow properties
    boundary_conditions = BoundaryConditions.WriteBoundaryConditions(properties, file_manager)
    boundary_conditions.write_all_appropriate_boundary_conditions()

    # write transport properties to file
    transport_dict = Transport.TransportPropertiesFile(properties, file_manager)
    transport_dict.write_input_file()

    # write turbulence properties to file
    turbulence_dict = Turbulence.TurbulencePropertiesFile(properties, file_manager)
    turbulence_dict.write_input_file()

    # write control dict file out
    control_dict = ControlDict.ControlDictFile(properties, file_manager)
    control_dict.write_input_file()

    # write fvSolution file out
    fv_solution = fvSolution.fvSolutionFile(properties, file_manager)
    fv_solution.write_input_file()

    # write fvSchemes
    fv_schemes = fvSchemes.fvSchemesFile(properties, file_manager)
    fv_schemes.write_input_file()

    # write additional files if required for on-the-fly post-processing
    if properties['dimensionless_coefficients']['write_force_coefficients']:
        force_coefficients = ForceCoefficients.WriteForceCoefficients(properties, file_manager)
        force_coefficients.write_force_coefficients()

    if properties['convergence_control']['integral_convergence_criterion'] != Parameters.NONE:
        force_coefficient_trigger = ForceCoefficientTrigger.WriteForceCoefficientConvergence(properties, file_manager)
        force_coefficient_trigger.write_triggers()

    if properties['dimensionless_coefficients']['write_pressure_coefficient']:
        pressure_coefficient = PressureCoefficient.WritePressureCoefficient(properties, file_manager)
        pressure_coefficient.write_force_coefficients()

    if properties['point_probes']['write_point_probes']:
        point_probes = PointProbes.WritePointProbes(properties, file_manager)
        point_probes.write_point_probes()

    if properties['line_probes']['write_line_probes']:
        line_probes = LineProbes.WriteLineProbes(properties, file_manager)
        line_probes.write_line_probes()

    if properties['cutting_planes']['write_cutting_planes']:
        cutting_planes = CuttingPlanes.WriteCuttingPlanes(properties, file_manager)
        cutting_planes.write_cutting_planes()

    if properties['iso_surfaces']['write_iso_surfaces']:
        iso_surfaces = IsoSurfaces.WriteIsoSurfaces(properties, file_manager)
        iso_surfaces.write_iso_surfaces()

    if properties['additional_fields']['write_additional_fields'] or properties['iso_surfaces']['write_iso_surfaces']:
        fields = AdditionalFields.WriteFields(properties, file_manager)
        fields.write_field()

    if properties['parallel_properties']['run_in_parallel']:
        decompose_par_dict = DecomposeParDict.WriteDecomposeParDictionary(properties, file_manager)
        decompose_par_dict.write_decompose_par_dict()

    y_plus = YPlus.WriteYPlus(properties, file_manager)
    y_plus.write_y_plus()

    residuals = Residuals.WriteResiduals(file_manager)
    residuals.write_residuals()

    # generate utility script class that produces useful scripts to run the simulation
    utility_scripts = UtilityScripts.WriteUtilityScripts(properties, file_manager)

    # write Allrun file to execute case automatically
    utility_scripts.write_all_run_file()

    # write Allclean file to clean up case directory
    utility_scripts.write_all_clean_file()

    # output diagnostics
    print('Generated case : ' + properties['file_properties']['path'])
    print('Reynolds number: ' + str(properties['flow_properties']['reynolds_number']))


if __name__ == '__main__':
    main()
