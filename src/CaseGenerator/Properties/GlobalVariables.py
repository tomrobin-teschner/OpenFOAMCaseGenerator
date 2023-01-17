from enum import Enum, auto

# coordinate directions
class Coordinates(Enum):
    x = 0
    y = auto()
    z = auto()

# mesh treatment
class Mesh(Enum):
    no_mesh = auto()
    block_mesh_dict = auto()
    snappy_hex_mesh_dict = auto()
    poly_mesh = auto()

# boundary condition ID
class BoundaryConditions(Enum):
    inlet = auto()
    dfsem_inlet = auto()
    freestream = auto()
    outlet = auto()
    backflow_outlet = auto()
    advective_outlet = auto()
    wall = auto()
    empty = auto()
    symmetry = auto()
    cyclic = auto()

# outlet boundary condition ID
# TODO: should be part of BoundaryConditions enum
class OutletBoundaryCondition(Enum):
    neumann = auto()
    advective = auto()
    inlet_outlet = auto()

# turbulence constant
# TODO: is this the right place here for c_mu?
class ClosureCoefficients(Enum):
    c_mu = 0.09

# flow type
class FlowType(Enum):
    incompressible = auto()
    compressible = auto()

# input parameter specification mode
class Dimensionality(Enum):
    dimensional = auto()
    non_dimensional = auto()

# solver to be used for solving the navier-stokes equation
class Solver(Enum):
    simpleFoam = auto()
    icoFoam = auto()
    pisoFoam = auto()
    pimpleFoam = auto()
    rhoCentralFoam = auto()
    rhoSimpleFoam = auto()
    rhoPimpleFoam = auto()
    sonicFoam = auto()

# solver to be used for solving the implicit system of equations for pressure
class PressureSolver(Enum):
    multi_grid = auto()
    krylov = auto()

# integral quantities used for convergence checking
class IntegralQuantities(Enum):
    Cd = auto()
    Cl = auto()
    Cs = auto()
    CmYaw = auto()
    CmRoll = auto()
    CmPitch = auto()
    coefficients_all = auto()
    coefficients_all_any = auto()

# start time for simulation
class SimulationStart(Enum):
    startTime = auto()
    firstTime = auto()
    latestTime = auto()

# output write control
class OutputWriteControl(Enum):
    timeStep = auto()
    runTime = auto()
    adjustableRunTime = auto()
    cpuTime = auto()
    clockTime = auto()

# time integration treatment
class TimeTreatment(Enum):
    steady_state = auto()
    unsteady = auto()

# numerical discretisation policy schemes
class DiscretisationPolicy(Enum):
    default = auto()
    tvd = auto()
    robustness = auto()
    accuracy = auto()

# simulation type
class TurbulenceType(Enum):
    laminar = auto()
    rans = auto()
    les = auto()

# wall modelling type
class WallModelling(Enum):
    low_re = 0
    high_re = auto()

# calculation of turbulent length scale
class TurbulenceLengthScaleCalculation(Enum):
    internal = auto()
    external = auto()
    ratio = auto()
    ratio_auto = auto()

# RANS models
class RansModel(Enum):
    kEpsilon = auto()
    realizableKE = auto()
    RNGkEpsilon = auto()
    LienLeschziner = auto()
    LamBremhorstKE = auto()
    LaunderSharmaKE = auto()
    kOmega = auto()
    kOmegaSST = auto()
    kOmegaSSTLM = auto()
    kkLOmega = auto()
    kOmegaSSTSAS = auto()
    qZeta = auto()
    SpalartAllmaras = auto()
    LienCubicKE = auto()
    ShihQuadraticKE = auto()
    LRR = auto()
    SSG = auto()

# LES models
class LesModel(Enum):
    Smagorinsky = auto()
    kEqn = auto()
    dynamicKEqn = auto()
    dynamicLagrangian = auto()
    DeardorffDiffStress = auto()
    WALE = auto()
    SpalartAllmarasDES = auto()
    SpalartAllmarasDDES = auto()
    SpalartAllmarasIDDES = auto()
    kOmegaSSTDES = auto()
    kOmegaSSTDDES = auto()
    kOmegaSSTIDDES = auto()

# LES filters
class LesFilter(Enum):
    simple = auto()
    anisotropic = auto()
    laplace = auto()

# LES delta models
class DeltaModel(Enum):
    smooth = auto()
    Prandtl = auto()
    maxDeltaxyz = auto()
    cubeRootVol = auto()
    maxDeltaxyzCubeRoot = auto()
    vanDriest = auto()
    IDDESDelta = auto()

# additional fields to write out during post-processing
class Fields(Enum):
    Q = auto()
    vorticity = auto()
    Lambda2 = auto()
    enstrophy = auto()

# initial conditions
class InitialConditions(Enum):
    boundary_condition_based = auto()
    zero_velocity = auto()
    custom = auto()

# field type
class FieldType(Enum):
    scalar = auto()
    vector = auto()
    tensor = auto()
