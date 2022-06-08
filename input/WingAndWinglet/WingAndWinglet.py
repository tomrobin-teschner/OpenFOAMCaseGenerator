import input.CasePropertiesBase as CPB
from src.Properties import GlobalVariables as Parameters
import os


class WingAndWinglet(CPB.CasePropertiesBase):
    @staticmethod
    def get_properties():
        return {
            'file_properties': {
                # name of the case to use (will be used for the folder name)
                'case_name': 'wing_and_winglet',

                # specify how the mesh should be incorporated into the case directory
                #   The following types are supported
                #   NO_MESH:                                Don't do anything, leave mesh treatment up to user
                #   BLOCK_MESH_DICT:                        Copy blockMeshDict file into case, requires the path to the
                #                                           file
                #   SNAPPY_HEX_MESH_DICT:                   Use snappyHexMesh for meshing. This may require a
                #                                           blockMeshDict file (or polyMesh directory) for the
                #                                           background mesh and a geometry file. Thus, the snappyHexMesh
                #                                           entry is a dictionary with optional entries which, if left
                #                                           empty, are ignored, otherwise additional files will be
                #                                           copied into the appropriate places and the Allrun script
                #                                           adjusted accordingly.
                #   POLY_MESH:                              Specify a polyMesh directory and copy it into the case setup
                'mesh_treatment': Parameters.SNAPPY_HEX_MESH_DICT,

                # directory where the blockMeshDict file is located (needs to be named blockMeshDict)
                'blockmeshdict_directory': os.path.join(''),

                # dictionary containing the required files for the snappyHexMesh setup. As a minimum, we need to specify
                # the folder containing the snappyHexMeshDict file. Additionally, we can specify either the
                # blockMeshDict file or the polyMesh directory for the background mesh. If we have a geometry as well
                # that the snappyHexMeshDict makes use of (potentially several files), then we can specify these in the
                # geometry entry. This is a list entry so that we can specify more than one geometry file. These will be
                # stored in within the constant/triSurface directory
                'snappyhexmeshdict': {
                    'snappyhexmesh_directory': os.path.join('examples', 'mesh', 'wing_and_winglet'),
                    'blockmeshdict_directory': os.path.join('examples', 'mesh', 'wing_and_winglet'),
                    'polymesh_directory': os.path.join(''),
                    'geometry': [
                        os.path.join('examples', 'geometry', 'wing_and_winglet', 'wing_and_winglet.stl'),
                    ]
                },

                # directory where the polyMesh is located (the specified directory needs to contain a folder called
                # polyMesh which in turn contains the boundary, cellZones, faces, faceZones, neighbour, owner and points
                # files)
                'polymesh_directory': os.path.join(''),

                # path to where the currently generated case should be copied to (parent directory)
                # if left empty, the case will be written into the current directory
                'run_directory': os.path.join(''),

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

            # properties imposed at boundaries / freestream
            'boundary_properties': {
                # define boundary conditions
                #   first  entry: name of boundary condition (specified in mesh generator)
                #   second entry: type of boundary condition (see below)
                #
                #   The following types are supported
                #   INLET:            Standard inlet condition, dirichlet for velocity + turbulence, neumann for
                #                     pressure
                #   DFSEM_INLET:      Divergence Free Synthetic Eddy Method (DFSEM) Inlet, use for Large-Eddy Simulation
                #                     to artificially create turbulent fluctuations at the inlet.
                #   FREESTREAM:       Specify freestream condition globally (can be inlet and outlet)
                #   OUTLET:           Standard outlet, fixed pressure and Neumann for velocity + turbulence
                #                     (Reflective outlet)
                #   BACKFLOW_OUTLET:  Same as outlet, but allows for flow to re-enter the domain (backflow at outlet)
                #   ADVECTIVE_OUTLET: Quantities are forced / advected outside domain (Non-reflective outlet)
                #   WALL:             Standard wall condition (ensure that the mesh has the type wall boundary assigned
                #                     instead of patch)
                #   EMPTY:            Used for essentially 2D simulations on the symmetry plane
                #   SYMMETRY:         Symmetry plane condition, i.e. wall with slip condition
                #                     (Neumann condition for all quantities)
                #   CYCLIC:           Use for periodic flows (mesh needs to have CYCLIC conditions defined)
                'boundary_conditions': {
                    'wing_and_winglet': Parameters.WALL,
                    'symmetry': Parameters.SYMMETRY,
                    'inlet': Parameters.FREESTREAM,
                    'outlet': Parameters.FREESTREAM,
                },

                # specify if custom inlet boundary conditions should be used for this case setup. If set to true, this
                # will require the dictionary entry for custom_inlet_boundary_conditions_setup
                'custom_inlet_boundary_conditions': False,

                # if custom inlet boundary conditions should be used, this dictionary provides a mapping where the key
                # is used to identify for which variable custom inlet boundary conditions should be written. The value
                # is a path to the c++ script which should be used as the custom inlet boundary condition
                'custom_inlet_boundary_conditions_setup': {
                    'variable': os.path.join('path', 'to', 'inlet', 'boundary', 'condition', 'script'),
                },

                # start DFSEM Inlet only section -----------------------------------------------------------------------
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

                # set turbulent length scale at inlet? If true, the turbulent length scale needs to be provided, if
                # false, we need to specify how many cells we want to use to resolve turbulent eddies (dynamically
                # adjust to the mesh size and controls the dissipation, use this option of no length scale information
                # is available). If custom_DFSEM_conditions is set to true and L is specified in
                # custom_DFSEM_conditions_setup, then this choice will have no effect
                'set_turbulent_length_scale_at_inlet': False,

                # turbulent length scale
                'turbulent_length_scale': 0.004,

                # number of cells to use to resolve turbulent eddies if no turbulent length scale is given. Typical
                # values should be between 1 - 5, where values closer to 1 are more dissipative and values closer to 5
                # sustain eddies for longer. Only used if both custom_DFSEM_conditions and
                # set_turbulent_length_scale_at_inlet are set to false.
                'number_of_cells_per_eddy': 1,
                # end DFSEM Inlet only section -------------------------------------------------------------------------
            },

            # physical properties of solver set-up
            'flow_properties': {
                # specify if custom initial conditions should be used for this case setup. If set to true, this will
                # require the dictionary entry for custom_initial_conditions_setup
                'custom_initial_conditions': False,

                # if custom initial conditions should be used, this dictionary provides a mapping where the key is
                # used to identify for which variable custom initial conditions should be written. The value is a
                # path to the c++ script which should be used as the custom initial condition
                'custom_initial_conditions_setup': {
                    'variable': os.path.join('path', 'to', 'initial', 'condition', 'script'),
                },

                # specify how the initial field should be set for non-custom initial conditions
                #   BOUNDARY_CONDITIONED_BASED: set the initial field based on inlet conditions (where applicable)
                #   ZERO_VELOCITY:              set the initial field to a zero velocity field
                'initial_conditions': Parameters.BOUNDARY_CONDITIONED_BASED,

                # type of the flow to solve
                #   The following types are supported:
                #     incompressible:   Solve the flow using a constant density approach
                #     compressible:     Solve the flow using a variable density approach
                'flow_type': Parameters.incompressible,

                # flag indicating whether viscosity should be constant or variable (only applicable to compressible
                # flows, in which case sutherland's law will be used to compute it)
                'const_viscosity': True,

                # specify whether input parameters should be specified using dimensional or non-dimensional parameters
                #   DIMENSIONAL:        Use dimensional quantities. Properties from the dimensional_properties
                #                       dictionary will be used
                #   NON_DIMENSIONAL:    Use non-dimensional quantities. Properties from the non_dimensional_properties
                #                       dictionary will be used
                'input_parameters_specification_mode': Parameters.DIMENSIONAL,

                # properties used when input parameters are specified using dimensional properties
                'non_dimensional_properties': {
                    # Reynolds number
                    'Re': 6000000,

                    # Mach number (only used for compressible flows)
                    'Ma': 0.15,
                },

                # properties used when input parameters are specified using dimensional properties
                'dimensional_properties': {
                    # specify the inlet velocity magnitude. The vector components will be constructed using the
                    # axis_aligned_flow_direction properties.
                    'velocity_magnitude': 10,

                    # specify density at inlet / freestream (only used for compressible calculations)
                    'rho': 1.0,

                    # specify the laminar viscosity (used for incompressible flows or compressible, if viscosity is set
                    # to const)
                    'nu': 1.46e-5,

                    # specify total pressure at inlet / freestream (ignored for incompressible flows, here,
                    # static pressure will be used and will be set to 0 by default)
                    'p': 0,

                    # specify temperature at inlet / freestream
                    'T': 288,
                },

                # specify the direction of the inflow velocity vector. Will be used to construct a 3D vector based on
                # the velocity magnitude. The tangential flow direction is aligned with the flow while the the normal
                # direction is perpendicular to it. To alter the direction within the plane that these two directions
                # span, use the angle_of_attack property. The property specified here will also be used to set up the
                # force coefficient calculation if required.
                'axis_aligned_flow_direction': {
                    'tangential': Parameters.X,
                    'normal': Parameters.Y,
                    'angle_of_attack': 5,
                },
            },

            'solver_properties': {
                # name of solver to use for solving the Navier-Stokes equations
                #   incompressible:
                #     simpleFoam:       steady state, turbulent (RANS) solver based on the SIMPLE algorithm
                #     icoFoam:          unsteady, non-turbulent (only laminar) solver based on the PISO algorithm
                #     pisoFoam:         unsteady, turbulent (RANS, LES) solver based on the PISO algorithm
                #     pimpleFoam:       unsteady, turbulent (RANS, LES) solver based on the SIMPLE + PISO algorithm.
                #                       May use higher CFL numbers than pisoFoam while being more stable.
                #                       Recommended in general
                #
                #   compressible:
                #     rhoCentralFoam:   Density-based compressible flow solver based on central-upwind schemes of
                #                       Kurganov and Tadmor
                #     rhoSimpleFoam:    Steady-state solver for compressible turbulent flow
                #     rhoPimpleFoam:    Transient solver for turbulent flow of compressible fluids for Heating,
                #                       ventilation, and air conditioning (HVAC) and similar applications, with optional
                #                       mesh motion and mesh topology changes
                #     sonicFoam:        Transient solver for trans-sonic/supersonic, turbulent flow of a compressible
                #                       gas
                'solver': Parameters.pimpleFoam,

                # number of times the non-orthogonal correction should be applied to the pressure equation. If the piso
                # or pimple algorithm is used, this will happen within each corrector step set below in
                # number_of_corrector_steps. If you have a cartesian mesh (i.e. no orthogonality) or only very small
                # non-orthogonality (perhaps less than 5 degree), use a value of 0. For mild non-orthogonality (below
                # 20 - 30 degree, typically achieved with a high quality structured grid) use one step.
                # For more general cases (e.g. unstructured grids or just higher values of non-orthogonality), use 2
                # non-orthogonal correction steps at most. More than two steps is unlikely to improve accuracy and will
                # only increase computational time.
                'number_of_non_orthogonal_corrector_steps': 2,

                # number of times the pressure equation and momentum corrector step should be solved. Used by the piso
                # and pimple algorithm only. Typically values are 2-3. A higher value can increase stability, a lower
                # value will speed up the computation. Stability is mesh and timestep / CFL number dependent.
                'number_of_corrector_steps': 2,

                # number of outer corrector steps (pimple only). This number will determine how many times we solve the
                # corrector step named above. If we set this value to 1, we recover the piso algorithm. A higher value
                # is advisable for CFL numbers larger than one for stability.
                'number_of_outer_corrector_steps': 1,

                # name of the solver to use to solve the implicit system of equations for the pressure
                #   MULTI_GRID:     Use OpenFOAM's geometric agglomerated algebraic multigrid (GAMG). May be less
                #                   efficient for parallel computations and non-elliptic flow problems
                #                   (e.g. compressible flows)
                #   KRYLOV:         Use OpenFOAM's Krylov subspace solver (Conjugate Gradient) with preconditioning.
                #                   Recommended to use for compressible and parallel computations
                'pressure_solver': Parameters.KRYLOV,

                # under-relaxation to be used by all fields and equations
                'under_relaxation_default': 0.7,

                # field-specific under-relaxation factors dictionary (leave empty if none) the key needs to be the
                # variable name such as p, U, T, rho, etc. and the value its under-relaxation factor
                'under_relaxation_fields': {
                },

                # equation-specific under-relaxation factors dictionary (leave empty if none) the key needs to be the
                # variable name such as p, U, T, rho, etc. and the value its under-relaxation factor
                'under_relaxation_equations': {
                },
            },

            'time_discretisation': {
                # time integration scheme, options are listed below
                #   STEADY_STATE: Do not integrate in time, i.e. dU / dt = 0
                #   UNSTEADY:     Integrate in time and resolve  dU / dt
                'time_integration': Parameters.STEADY_STATE,

                # these properties will be used if time_integration is set to Parameters.STEADY_STATE above
                'steady_state_properties': {
                    # specify from which time directory to start from
                    #   START_TIME:  Start from the folder that is defined in the startTime variable
                    #   FIRST_TIME:  Start from the first available (lowest time) directory
                    #   LATEST_TIME: Start from the latest available (highest time) directory. Use to restart a
                    #                simulation from the last calculated solution
                    'startFrom': Parameters.START_TIME,

                    # start time
                    'startTime': 0,

                    # end time
                    'endTime': 2000,

                    # flag indicating whether to dynamically calculate time step based on CFL criterion
                    'CFLBasedTimeStepping': False,

                    # CFL number
                    'CFL': 1.0,

                    # time step to be used (will be ignored if CFL-based time stepping is chosen)
                    # WARNING: solver needs to support adjustable deltaT calculation
                    'deltaT': 1,

                    # largest allowable time step
                    'maxDeltaT': 1,

                    # write control, specify when to output results, the options are listed below
                    #   TIME_STEP:           write every 'write_frequency' time steps
                    #   RUN_TIME:            write data every 'write_frequency' seconds of simulated time
                    #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
                    #                        (use with 'CFLBasedTimeStepping' = True)
                    #   CPU_TIME:            write data every 'write_frequency' seconds of CPU time
                    #   CLOCK_TIME:          write data every 'write_frequency' seconds of real time
                    'write_control': Parameters.TIME_STEP,

                    # frequency at which to write output files. Behaviour controlled through write control entry above.
                    'write_frequency': 250,

                    # specify how many solutions to keep (specify 0 to keep all)
                    'purge_write': 0,
                },

                # these properties will be used if time_integration is set to Parameters.UNSTEADY above
                'unsteady_properties': {
                    # specify from which time directory to start from
                    #   START_TIME:  Start from the folder that is defined in the startTime variable
                    #   FIRST_TIME:  Start from the first available (lowest time) directory
                    #   LATEST_TIME: Start from the latest available (highest time) directory. Use to restart a
                    #                simulation from the last calculated solution
                    'startFrom': Parameters.START_TIME,

                    # start time
                    'startTime': 0,

                    # end time
                    'endTime': 1,

                    # flag indicating whether to dynamically calculate time step based on CFL criterion
                    'CFLBasedTimeStepping': True,

                    # CFL number
                    'CFL': 1.0,

                    # time step to be used (will be ignored if CFL-based time stepping is chosen)
                    # WARNING: solver needs to support adjustable deltaT calculation
                    'deltaT': 1e-4,

                    # largest allowable time step
                    'maxDeltaT': 1,

                    # write control, specify when to output results, the options are listed below
                    #   TIME_STEP:           write every 'write_frequency' time steps
                    #   RUN_TIME:            write data every 'write_frequency' seconds of simulated time
                    #   ADJUSTABLE_RUN_TIME: same as RUN_TIME, but may adjust time step for nice values
                    #                        (use with 'CFLBasedTimeStepping' = True)
                    #   CPU_TIME:            write data every 'write_frequency' seconds of CPU time
                    #   CLOCK_TIME:          write data every 'write_frequency' seconds of real time
                    'write_control': Parameters.ADJUSTABLE_RUN_TIME,

                    # frequency at which to write output files. Behaviour controlled through write control entry above.
                    'write_frequency': 0.01,

                    # specify how many solutions to keep (specify 0 to keep all)
                    'purge_write': 0,
                },
            },

            'spatial_discretisation': {
                # Choose preset of numerical schemes based on accuracy and robustness requirements
                #   DEFAULT:    Optimal trade-off between accuracy and stability. Recommended for most cases. Tries to
                #               achieve second-order accuracy.
                #   TVD:        Same as DEFAULT, but use bounded Total Variation Diminishing (TVD) schemes instead of
                #               upwind schemes
                #   ROBUSTNESS: Use this option if your simulation does not converge or your mesh has bad mesh quality
                #               metrics. First-order accurate in space and time
                #   ACCURACY:   Recommended for accuracy and scale resolved simulations (LES, DES, SAS). May be used
                #               after running a simulation with DEFAULT or ROBUSTNESS to increase accuracy. Second-order
                #               accurate with less limiting compared to DEFAULT and TVD.
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
                #   LOW_RE  : first cell-height near wall is of the order y+ <= 1
                #   HIGH_RE : first cell-height near wall is of the order y+ >  30
                'wall_modelling': Parameters.HIGH_RE,

                # select how to calculate turbulent quantities at inlet
                #   INTERNAL:    Internal flow assumes the turbulent length scale to be limited by the channel /
                #                wind tunnel height or diameter, expressed through the reference_length parameter.
                #                It is calculated as 0.07 * reference length
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

                # freestream turbulent intensity (between 0 - 1), used for RANS initial and boundary conditions
                'freestream_turbulent_intensity': 0.05,

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
                #     WALE:                 The Wall-adapting local eddy-viscosity (WALE) SGS model
                #
                #   DES:
                #     SpalartAllmarasDES:   Detached Eddy Simulation based on the Spalart-Allmaras model
                #     SpalartAllmarasDDES:  Delayed Detached Eddy Simulation based on the Spalart-llmaras model
                #     SpalartAllmarasIDDES: Improved Delayed Detached Eddy Simulation based on the Spalart-Allmaras
                #                           model
                #     kOmegaSSTDES:         Detached Eddy Simulation based on the k-omega SST model
                #     kOmegaSSTDDES:        Delayed Detached Eddy Simulation based on the k-omega SST model
                #     kOmegaSSTIDDES:       Improved Delayed Detached Eddy Simulation based on the k-omega SST model
                'LES_model': Parameters.kEqn,

                # filter for spatial LES filtering, used for dynamic subgrid-scale models
                #   SIMPLE_FILTER:      Simple top-hat filter used in dynamic LES models
                #   ANISOTROPIC_FILTER: Anisotropic filter
                #   LAPLACE_FILTER:     Laplace filter
                'LES_filter': Parameters.SIMPLE_FILTER,

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
                # convergence criterion for residuals (used to judge if a simulation has converged to a steady state)
                'convergence_threshold': 1e-6,

                # absolute convergence criterion for implicit solvers (used to judge if the current iteration has
                # converged)
                'absolute_convergence_criterion': 1e-14,

                # relative convergence criterion for implicit solvers
                #
                # NOTE: For steady state simulations, we don't have to converge fully within each iteration so a low
                # relative tolerance may be chosen (e.g. 0.01). For unsteady flows, we need to have an accurate
                # prediction within each time step and we should take a lower value here (e.g. 1e-6) to avoid diffusive
                # results in time
                'relative_convergence_criterion': 1e-2,

                # check if an integral quantity has converged instead of just checking the residuals.
                # Recommended if such a integral quantity can be easily defined for the current simulation.
                # If no quantity is specified (i.e. we have an empty list), no convergence checking is performed.
                #   C_D:                  Convergence criterion based on the drag force coefficient
                #   C_L:                  Convergence criterion based on the lift force coefficient
                #   C_S:                  Convergence criterion based on the side force coefficient
                #   C_M_YAW:              Convergence criterion based on the yaw momentum coefficient
                #   C_M_ROLL:             Convergence criterion based on the roll momentum coefficient
                #   C_M_PITCH:            Convergence criterion based on the pitch momentum coefficient
                'integral_convergence_criterion': [Parameters.C_D, Parameters.C_L],

                # if integral quantities are checked for convergence, specify for how many timesteps their average
                # should be calculated to check if, on average, the quantity has converged
                'averaging_time_steps': 20,

                # specify the convergence threshold for the integral quantities
                'integral_quantities_convergence_threshold': 1e-5,

                # specify how many iterations to wait before checking convergence criterion
                'time_steps_to_wait_before_checking_convergence': 100,
            },

            'dimensionless_coefficients': {
                # reference length (used for RANS initial and boundary conditions)
                'reference_length': 0.34,

                # reference area (used to non-dimensionalise force coefficients)
                'reference_area': 0.326,

                # center of rotation for momentum coefficient
                'center_of_rotation': [0.25, 0, 0],

                # group of wall boundaries, which should be used to calculate force coefficients on (enter as list)
                'wall_boundaries': ['wing_and_winglet'],

                # write force coefficients to file
                'write_force_coefficients': True,

                # write pressure coefficient (cp) to file
                'write_pressure_coefficient': True,

                # write wall shear stresses (can be used to obtain skin friction coefficient) to file
                'write_wall_shear_stresses': False,
            },

            # write out additional fields of interest
            'additional_fields': {
                # flag indicating if additional fields should be active (written to file). Will be written with all
                # other variables to file at the same time. If set to false, ignore the rest of this dictionary.
                'write_additional_fields': False,

                # list of additional fields to write, can be more than 1 (Mach number will be automatically written for
                # compressible flow cases)
                #   Q:         Write out the Q-criterion, useful for isoSurfaces to visualise turbulence structures
                #   VORTICITY: Write out vorticity field
                #   LAMBDA_2:  Write out the Lambda-2 criterion, useful for vortex core detection
                #   ENSTROPHY: Write out enstrophy field
                'fields': [Parameters.Q, Parameters.VORTICITY],
            },

            # specify 0-D point probes to which will output flow variables at each timestep at a given location x,
            # y and z
            'point_probes': {
                # flag indicating if point probes should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_point_probes': False,

                # specify the location at which to output information, can be more than 1
                'location': [
                    [1, 0.01, 0],
                    [2, 0, 0],
                ],

                # specify variables that should be monitored at the specified point
                'variables_to_monitor': ['U', 'p'],

                # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only
                # be written according to the settings in the controlDict (i.e. every time a new time directory is
                # generated)
                'output_probe_at_every_timestep': True,
            },

            # specify 1-D line probes
            'line_probes': {
                # flag indicating if point probes should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
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

                # if flag is set to true, solution will be written at every time step. Otherwise, the probe will only
                # be written according to the settings in the controlDict (i.e. every time a new time directory is
                # generated)
                'output_probe_at_every_timestep': False,
            },

            # specify 2-D cutting planes
            'cutting_planes': {
                # flag indicating if point probes should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_cutting_planes': False,

                # specify the origin and normal vector of cutting plane, can be more than 1
                'location': [
                    {
                        'name': 'plane_x=0',
                        'origin': [0, 0, 0],
                        'normal': [1, 0, 0],
                    },
                    {
                        'name': 'plane_y=0',
                        'origin': [0, 0, 0],
                        'normal': [0, 1, 0],
                    },
                    {
                        'name': 'plane_z=0',
                        'origin': [0, 0, 0],
                        'normal': [0, 0, 1],
                    },
                ],

                # specify variables that should be monitored along line
                'variables_to_monitor': ['U', 'p', 'vorticity'],

                # if flag is set to true, solution will be written at every time step. Otherwise, the cutting plane will
                # only be written according to the settings in the controlDict (i.e. every time a new time directory is
                # generated)
                'output_cutting_plane_at_every_timestep': False,
            },

            # write iso surfaces of variables during calculation
            'iso_surfaces': {
                # flag indicating if iso-surfaces should be active (written to file). If set to false, ignore the
                # rest of this dictionary.
                'write_iso_surfaces': False,

                # variables of which to write iso surfaces
                'flow_variable': ['Q'],

                # iso value at which point the surface should be written. List entry correspond to order specified in
                # flow_variable list
                'iso_value': [0.1],

                # additional fields to write (can be more than 1, can be used to colour iso-surface in post-processing)
                'additional_field_to_write': ['p'],

                # if flag is set to true, iso-surfaces will be written at every time step. Otherwise,
                # the iso surfaces will only be written according to the settings in the controlDict (i.e. every time
                # a new time directory is generated)
                'output_iso_surfaces_at_every_timestep': False,
            },

            # user-defined function objects that will get executed after all other function objects have run
            'post_processing': {
                # execute user-defined function object?
                'execute_function_object': False,

                # path to user-defined function object as a key value pair (dictionary). The key is used as the name of
                # the file and the value is the path to the function object that should be executed
                'function_objects': {
                    'functionObject': os.path.join('')
                },

                # execute user-defined post processing routines?
                'execute_python_script': False,

                # list of user defined python scripts to copy and execute after the simulation is done
                # each list entry contains a dictionary with 2 key-value pairs. The first key is named "script" and
                # needs to point to the location of the python script. The second is the "requires" key which is a list
                # of files requires by the script, for example, reference solution data that is read by the script
                'python_script': [
                    {
                        'script': os.path.join(''),
                        'requires': [
                            os.path.join(''),
                        ],
                    },
                ],
            },
        }
