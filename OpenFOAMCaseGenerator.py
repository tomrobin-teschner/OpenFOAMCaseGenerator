import os
from math import sqrt, pow
import json

import src.FileDirectoryIO.FileManager as IO
import src.FileDirectoryIO.WriteUtilityScripts as UtilityScripts
import src.FileDirectoryIO.ScreenOutput as ScreenOutput
from src.CheckCase import CheckCase as CheckCase
from src.CheckCase import CheckCommandLineArguments as CheckCommandLineArguments
import src.WriteSystemDirectoryFiles.WriteForceCoefficients as ForceCoefficients
import src.WriteSystemDirectoryFiles.WritePressureCoefficient as PressureCoefficient
import src.WriteSystemDirectoryFiles.WriteDecomposePar as DecomposeParDict
import src.WriteSystemDirectoryFiles.WriteYPlus as YPlus
import src.WriteSystemDirectoryFiles.WriteResiduals as Residuals
import src.WriteSystemDirectoryFiles.WriteForceCoefficientConvergence as ForceCoefficientTrigger
import src.WriteSystemDirectoryFiles.WritePointProbes as PointProbes
import src.WriteSystemDirectoryFiles.WriteLineProbes as LineProbes
import src.WriteSystemDirectoryFiles.WriteCuttingPlanes as CuttingPlanes
import src.WriteSystemDirectoryFiles.WriteFields as AdditionalFields
import src.WriteSystemDirectoryFiles.WriteIsoSurfaces as IsoSurfaces
from src import GlobalVariables as Parameters

import src.WriteConstantDirectoryFiles.WriteTransportProperties as Transport
import src.WriteConstantDirectoryFiles.WriteTurbulenceProperties as Turbulence
import src.WriteSystemDirectoryFiles.WriteControlDictFile as ControlDict
import src.WriteSystemDirectoryFiles.WritefvSolutionFile as fvSolution
import src.WriteSystemDirectoryFiles.WritefvSchemesFile as fvSchemes
import src.Write0DirectoryFiles.WriteBoundaryConditions as BoundaryConditions


def case_properties(command_line_arguments):
    properties = {
        'file_properties': {
            # name of the case to use (will be used for the folder name)
            'case_name': 'square_cylinder_Re=40',

            # specify how the mesh should be incorporated into the case directory
            #   The following types are supported
            #   NO_MESH:                                Don't do anything, leave mesh treatment up to user
            #   BLOCK_MESH_DICT:                        Copy blockMeshDict file into case, requires the path to the file
            #   BLOCK_MESH_AND_SNAPPY_HEX_MESH_DICT:    Copy both blockMeshDict and snappyHexMeshDict to directory,
            #                                           requires the path to both files
            #   POLY_MESH:                              Specify a polyMesh directory and copy it into the case setup
            'mesh_treatment': Parameters.POLY_MESH,

            # directory where the blockMeshDict file is located (needs to be named blockMeshDict)
            'blockmeshdict_directory': os.path.join(''),

            # directory where the snappyHexMeshDict file is located (needs to be named snappyHexMeshDict)
            'snappyhexmeshdict_directory': os.path.join(''),

            # directory where the polyMesh is located (the specified directory needs to contain a folder called polyMesh
            # which in turn contains the boundary, cellZones, faces, faceZones, neighbour, owner and points files)
            'polymesh_directory': os.path.join('examples', 'mesh', 'square_cylinder'),

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
        #   DFSEM_INLET:      Divergence Free Synthetic Eddy Method (DFSEM) Inlet, use for Large-Eddy Simulation to
        #                     artificially create turbulent fluctuations at the inlet.
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
            'symmetry': Parameters.SYMMETRY,
            'BaseAndTop': Parameters.EMPTY,
        },

        # physical properties of solver set-up
        'flow_properties': {
            # specify if custom initial conditions should be used for this case setup. If set to true, this will require
            # the dictionary entry for custom_initial_conditions_setup
            'custom_initial_conditions': False,

            # if custom initial conditions should be used, this dictionary provides a mapping where the key is used to
            # identify for which variable custom initial conditions should be written. The value is a path to the c++
            # script which should be used as the custom initial condition
            'custom_initial_conditions_setup': {
                'p': os.path.join('examples', 'scripts', 'initialConditions', 'taylorGreenVortex', 'p'),
                'U': os.path.join('examples', 'scripts', 'initialConditions', 'taylorGreenVortex', 'U'),
            },

            # specify if custom inlet boundary conditions should be used for this case setup. If set to true, this will
            # require the dictionary entry for custom_inlet_boundary_conditions_setup
            'custom_inlet_boundary_conditions': False,

            # if custom inlet boundary conditions should be used, this dictionary provides a mapping where the key is
            # used to identify for which variable custom inlet boundary conditions should be written. The value is a
            # path to the c++ script which should be used as the custom inlet boundary condition
            'custom_inlet_boundary_conditions_setup': {
                'p': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'scalarField'),
                'U': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'vectorField'),
            },

            # specify the inlet boundary condition (free stream velocity). This is only used if no custom inlet
            # boundary conditions are used for the velocity.
            'inlet_velocity': [4.0, 0, 0],

            # specify how the initial field should be set for non-custom initial conditions
            #   BOUNDARY_CONDITIONED_BASED: set the initial field based on inlet conditions (where applicable)
            #   ZERO_VELOCITY:              set the initial field to a zero velocity field
            'initial_conditions': Parameters.BOUNDARY_CONDITIONED_BASED,

            # specify the laminar viscosity
            'nu': 1e-1,

            # freestream turbulent intensity (between 0 - 1)
            'freestream_turbulent_intensity': 0.05,

            # reference length in simulation
            'reference_length': 1.0,

            # start DFSEM Inlet only section ---------------------------------------------------------------------------
            # the below options are for the special DFSEM Inlet only. Use with caution. Before using, see remarks at
            # https://www.cfd-online.com/Forums/openfoam-solving/177711-turbulentdfseminlet.html

            # specify whether custom inlet or freestream conditions should be set
            'custom_DFSEM_conditions': False,

            # if custom DFSEM conditions should be set, specify the path which the custom conditions are stored
            'custom_DFSEM_conditions_setup': {
                'R': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'tensorField'),
                'U': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'vectorField'),
                'L': os.path.join('examples', 'scripts', 'boundaryConditions', 'generic', 'scalarField'),
            },

            # specify the reynold stresses at the inlet, ignored if custom_DFSEM_conditions is set to True and R is
            # specified in custom_DFSEM_conditions_setup. The order is R_uu, R_uv, R_uw, R_vv, R_vw, R_ww
            'reynolds_stresses': [1, 0, 0, 0, 0, 0],

            # set turbulent length scale at inlet? If true, the turbulent length scale needs to be provided, if false,
            # we need to specify how many cells we want to use to resolve turbulent eddies (dynamically adjust to the
            # mesh size and controls the dissipation, use this option of no length scale information is available)
            # If custom_DFSEM_conditions is set to true and L is specified in custom_DFSEM_conditions_setup, then this
            # choice will have no effect
            'set_turbulent_length_scale_at_inlet': False,

            # turbulent length scale
            'turbulent_length_scale': 0.004,

            # number of cells to use to resolve turbulent eddies if no turbulent length scale is given. Typical values
            # should be between 1 - 5, where values closer to 1 are more dissipative and values closer to 5 sustain
            # eddies for longer. Only used if both custom_DFSEM_conditions and set_turbulent_length_scale_at_inlet
            # are set to false.
            'number_of_cells_per_eddy': 1,
            # end DFSEM Inlet only section -----------------------------------------------------------------------------
        },

        'solver_properties': {
            # name of solver to use for solving the Navier-Stokes equations
            #   incompressible:
            #     simpleFoam: steady state, turbulent (RANS) solver based on the SIMPLE algorithm
            #     icoFoam:    unsteady, non-turbulent (only laminar) solver based on the PISO algorithm
            #     pisoFoam:   unsteady, turbulent (RANS, LES) solver based on the PISO algorithm
            #     pimpleFoam: unsteady, turbulent (RANS, LES) solver based on the SIMPLE + PISO algorithm. May use
            #                 higher CFL numbers than pisoFoam while being more stable. Recommended in general
            'solver': Parameters.pimpleFoam,

            # name of the solver to use to solve the implicit system of equations for the pressure
            #   MULTI_GRID:     Use OpenFOAM's geometric agglomerated algebraic multigrid (GAMG). May be less efficient
            #                   for parallel computations and non-elliptic flow problems (e.g. compressible flows)
            #   KRYLOV:         Use OpenFOAM's Krylov subspace solver (Conjugate Gradient) with preconditioning.
            #                   Recommended to use for compressible and parallel computations
            'pressure_solver':  Parameters.KRYLOV,

            # start time
            'startTime': 0,

            # end time
            'endTime': 1,

            # specify from which time directory to start from
            #   START_TIME:  Start from the folder that is defined in the startTime variable
            #   FIRST_TIME:  Start from the first available (lowest time) directory
            #   LATEST_TIME: Start from the latest available (highest time) directory. Use to restart a simulation from
            #                the last calculated solution
            'startFrom': Parameters.START_TIME,

            # flag indicating whether to dynamically calculate time step based on CFL criterion
            'CFLBasedTimeStepping': True,

            # CFL number
            'CFL': 1.0,

            # time step to be used (will be ignored if CFL-based time stepping is chosen)
            # WARNING: solver needs to support adjustable deltaT calculation
            'deltaT': 2e-3,

            # largest allowable time step
            'maxDeltaT': 1,

            # frequency at which to write output files. Behaviour controlled through write control entry below.
            'write_frequency': 0.1,

            # write control, specify when to output results, the options are listed below
            #   TIME_STEP:           write every 'write_frequency' time steps
            #   RUN_TIME:            write data every 'write_frequency' seconds of simulated time
            #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
            #                        (use with 'CFLBasedTimeStepping' = True)
            #   CPU_TIME:            write data every 'write_frequency' seconds of CPU time
            #   CLOCK_TIME:          write data every 'write_frequency' seconds of real time
            'write_control': Parameters.ADJUSTABLE_RUN_TIME,

            # specify how many solutions to keep (specify 0 to keep all)
            'purge_write': 0,

            # under-relaxation factor for pressure
            'under_relaxation_p': 0.7,

            # under-relaxation factor for velocity
            'under_relaxation_U': 0.7,

            # under-relaxation factor for turbulent quantities
            'under_relaxation_turbulence': 0.7,

            # under-relaxation factor for Reynolds stresses
            'under_relaxation_reynolds_stresses': 0.3,
        },

        'numerical_discretisation': {
            # time integration scheme, options are listed below
            #   STEADY_STATE: Do not integrate in time, i.e. dU / dt = 0
            #   UNSTEADY:     Integrate in time and resolve  dU / dt
            'time_integration': Parameters.UNSTEADY,

            # Choose preset of numerical schemes based on accuracy and robustness requirements
            #   DEFAULT:    Optimal trade-off between accuracy and stability. Recommended for most cases. Tries to
            #               achieve second-order accuracy.
            #   TVD:        Same as DEFAULT, but use Total Variation Diminishing (TVD) schemes instead of upwind schemes
            #   ROBUSTNESS: Use this option if your simulation does not converge or your mesh has bad mesh quality
            #               metrics. First-order accurate in space and time
            #   ACCURACY:   Recommended for accuracy and scale resolved simulations (LES, DES, SAS). May be used after
            #               running a simulation with DEFAULT or ROBUSTNESS to increase accuracy. Second-order accurate
            #               with less limiting compared to DEFAULT and TVD.
            'numerical_schemes_correction': Parameters.DEFAULT,

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
            #     Smagorinsky:          Large Eddy Simulation based on classical Smagorinsky approach (fixed C_s)
            #     kEqn:                 One equation eddy-viscosity model
            #                           Eddy viscosity SGS model using a modeled balance equation to simulate the
            #                           behaviour of k.
            #     dynamicKEqn:          Dynamic one equation eddy-viscosity model
            #                           Eddy viscosity SGS model using a modeled balance equation to simulate
            #                           the behaviour of k in which a dynamic procedure is applied to evaluate the
            #                           coefficients
            #     dynamicLagrangian:    Dynamic SGS model with Lagrangian averaging
            #     DeardorffDiffStress:  Differential SGS Stress Equation Model for incompressible and
            #                           compressible flows
            #     WALE:                 The Wall-adapting local eddy-viscosity (WALE) SGS model
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
            #   smooth:                 Smoothed delta which takes a given simple geometric delta and applies
            #                           smoothing to it such that the ratio of deltas between two cells is no
            #                           larger than a specified amount, typically 1.15
            #   Prandtl:                Apply Prandtl mixing-length based damping function to the specified
            #                           geometric delta to improve near-wall behavior or LES models
            #   maxDeltaxyz:            Delta calculated by taking the maximum distance between the cell centre
            #                           and any face centre.  For a regular hex cell, the computed delta will
            #                           equate to half of the cell width; accordingly, the deltaCoeff model
            #                           coefficient should be set to 2 for this case
            #   cubeRootVol:            Simple cube-root of cell volume delta used in LES models
            #   maxDeltaxyzCubeRoot:    Maximum delta between maxDeltaxyz and cubeRootVolDelta
            #   vanDriest:              Simple cube-root of cell volume delta used in incompressible LES models
            #   IDDESDelta:             IDDESDelta used by the IDDES (improved low Re Spalart-Allmaras DES model)
            #                           The min and max delta are calculated using the face to face distance of
            #                           the cell
            'delta_model': Parameters.cubeRootVol,
        },

        'convergence_control': {
            # convergence criterion for residuals (used to judge if a simulation has converged)
            'convergence_threshold': 1e-4,

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
            'integral_convergence_criterion': Parameters.C_L,

            # if integral quantities are checked for convergence, specify for how many timesteps their average should be
            # calculated to check if, on average, the quantity has converged
            'averaging_time_steps': 20,

            # specify the convergence threshold for the integral quantities
            'integral_quantities_convergence_threshold': 1e-3,

            # specify how many iterations to wait before checking convergence criterion
            'time_steps_to_wait_before_checking_convergence': 100,
        },

        'dimensionless_coefficients': {
            # reference area used to non-dimensionalise force coefficients
            'reference_area': 1,

            # direction of lift vector (normalised to unity)
            'lift_direction': [0, 1, 0],

            # direction of drag vector (normalised to unity)
            'drag_direction': [1, 0, 0],

            # direction of pitch axis for momentum coefficient (normalised to unity)
            'pitch_axis_direction': [0, 0, 1],

            # center of rotation for momentum coefficient
            'center_of_rotation': [0.25, 0, 0],

            # group of wall boundaries, which should be used to calculate force coefficients on (enter as list)
            'wall_boundaries': ['wall'],

            # write force coefficients to file
            'write_force_coefficients': True,

            # write pressure coefficient (cp) to file
            'write_pressure_coefficient': False,

            # write wall shear stresses (can be used to obtain skin friction coefficient) to file
            'write_wall_shear_stresses': False,
        },

        # write out additional fields of interest
        'additional_fields': {
            # flag indicating if additional fields should be active (written to file). Will be written with all other
            # variables to file at the same time. If set to false, ignore the rest of this dictionary.
            'write_additional_fields': False,

            # list of additional fields to write, can be more than 1
            #   Q:         Write out the Q-criterion, useful for isoSurfaces to visualise turbulence structures
            #   VORTICITY: Write out vorticity field
            #   LAMBDA_2:  Write out the Lambda-2 criterion, useful for vortex core detection
            #   ENSTROPHY: Write out enstrophy field (useful for turbulent studies)
            'fields': [Parameters.Q, Parameters.VORTICITY],
        },

        # specify 0-D point probes to which will output flow variables at each timestep at a given location x, y and z
        'point_probes': {
            # flag indicating if point probes should be active (written to file). If set to false, ignore the rest of
            # this dictionary.
            'write_point_probes': False,

            # specify the location at which to output information, can be more than 1
            'location': [
                [1, 0.01, 0],
                [2, 0, 0],
            ],

            # specify variables that should be monitored at the specified point
            'variables_to_monitor': ['U', 'p'],

            # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only be
            # written according to the settings in the controlDict (i.e. every time a new time directory is generated)
            'output_probe_at_every_timestep': True,
        },

        # specify 1-D line probes
        'line_probes': {
            # flag indicating if point probes should be active (written to file). If set to false, ignore the rest of
            # this dictionary.
            'write_line_probes': False,

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

            # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only be
            # written according to the settings in the controlDict (i.e. every time a new time directory is generated)
            'output_probe_at_every_timestep': False,
        },

        # specify 2-D cutting planes
        'cutting_planes': {
            # flag indicating if point probes should be active (written to file). If set to false, ignore the rest of
            # this dictionary.
            'write_cutting_planes': False,

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

            # if flag is set to true, solution will be written at every time step. Otherwise, the cutting plane will
            # only be written according to the settings in the controlDict (i.e. every time a new time directory is
            # generated)
            'output_cutting_plane_at_every_timestep': False,
        },

        # write iso surfaces of variables during calculation
        'iso_surfaces': {
            # flag indicating if iso-surfaces should be active (written to file). If set to false, ignore the rest of
            # this dictionary.
            'write_iso_surfaces': False,

            # variables of which to write iso surfaces
            'flow_variable': ['Q', 'Lambda2'],

            # iso value at which point the surface should be written. List entry correspond to order specified in
            # flow_variable list
            'iso_value': [1e-5, 0],

            # additional fields to write (can be more than 1, can be used to colour iso-surface in post-processing)
            'additional_field_to_write': ['p'],

            # if flag is set to true, iso-surfaces will be written at every time step. Otherwise, the iso surfaces will
            # only be written according to the settings in the controlDict (i.e. every time a new time directory is
            # generated)
            'output_iso_surfaces_at_every_timestep': False,
        },
    }

    # process properties dictionary (read and write if necessary)
    if command_line_arguments.option_exists('input'):
        with open(command_line_arguments['input'], 'r') as json_file:
            properties = json.load(json_file)
    elif command_line_arguments.option_exists('output'):
        with open(command_line_arguments['output'], 'w') as json_file:
            json.dump(properties, json_file, indent=4)
    elif command_line_arguments.option_exists('write-json-only'):
        with open(command_line_arguments['write-json-only'], 'w') as json_file:
            json.dump(properties, json_file, indent=4)
        exit(0)

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

    # process command line arguments first
    command_line_arguments = CheckCommandLineArguments.CheckCommandLineArguments()

    # get case specific dictionaries to set up case and write input files
    properties = case_properties(command_line_arguments)

    # check case (make sure that current set up will not produce any problem)
    check_case = CheckCase.CheckCase(properties)
    check_case.run_all_checks()

    # add additional entries to dictionaries
    add_default_properties(properties)

    # create the initial data structure for the case set-up
    file_manager = IO.FileManager(properties)
    file_manager.create_directory_structure()
    file_manager.copy_mesh_to_destination()

    # write out boundary conditions for all relevant flow properties
    boundary_conditions = BoundaryConditions.WriteBoundaryConditions(properties, file_manager)
    boundary_conditions.write_all_boundary_conditions()

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
    screen_output = ScreenOutput.ScreenOutput(properties)
    screen_output.print_summary()


if __name__ == '__main__':
    main()
