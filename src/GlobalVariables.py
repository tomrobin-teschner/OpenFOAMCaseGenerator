# coordinate directions
X = 0
Y = 1
Z = 2

# mesh treatment
NO_MESH = 0
BLOCK_MESH_DICT = 1
BLOCK_MESH_AND_SNAPPY_HEX_MESH_DICT = 2
POLY_MESH = 3

# boundary condition ID
INLET = 0
DFSEM_INLET = 1
FREESTREAM = 2
OUTLET = 3
BACKFLOW_OUTLET = 4
ADVECTIVE_OUTLET = 5
WALL = 6
EMPTY = 7
SYMMETRY = 8
CYCLIC = 9

# boundary properties stored in boundary condition class
BC_TYPE = 0
BC_DIMENSIONS = 1

# outlet boundary condition ID
NEUMANN = 0
ADVECTIVE = 1
INLET_OUTLET = 2

# turbulence constant
C_MU = 0.09

# flow type
incompressible = 0
compressible = 1

# input parameter specification mode
DIMENSIONAL = 0
NON_DIMENSIONAL = 1

# solver to be used for solving the navier-stokes equation
simpleFoam = 0
icoFoam = 1
pisoFoam = 2
pimpleFoam = 3
rhoCentralFoam = 4
rhoSimpleFoam = 5
rhoPimpleFoam = 6
sonicFoam = 7

# solver to be used for solving the implicit system of equations for the pressure
MULTI_GRID = 0
KRYLOV = 1

# integral quantities used for convergence checking
NONE = -1
C_D = 0
C_L = 1
C_S = 2
C_M_YAW = 3
C_M_ROLL = 4
C_M_PITCH = 5
COEFFICIENTS_ALL = 6
COEFFICIENTS_ALL_ANY = 7

# start time for simulation
START_TIME = 0
FIRST_TIME = 1
LATEST_TIME = 2

# output write control
TIME_STEP = 0
RUN_TIME = 1
ADJUSTABLE_RUN_TIME = 2
CPU_TIME = 3
CLOCK_TIME = 4

# numerical schemes
STEADY_STATE = 0
UNSTEADY = 1

# stability controlling parameter for gradient schemes
DEFAULT = 0
TVD = 1
ROBUSTNESS = 2
ACCURACY = 3

# simulation type
LAMINAR = 0
RANS = 1
LES = 2

# wall modelling type
LOW_RE = 0
HIGH_RE = 1

# calculation of turbulent length scale
INTERNAL = 0
EXTERNAL = 1
RATIO = 2
RATIO_AUTO = 3

# RANS models
kEpsilon = 0
realizableKE = 1
RNGkEpsilon = 2
LienLeschziner = 3
LamBremhorstKE = 4
LaunderSharmaKE = 5
kOmega = 6
kOmegaSST = 7
kOmegaSSTLM = 8
kkLOmega = 9
kOmegaSSTSAS = 10
qZeta = 11
SpalartAllmaras = 12
LienCubicKE = 13
ShihQuadraticKE = 14
LRR = 15
SSG = 16

# LES models
Smagorinsky = 0
kEqn = 1
dynamicKEqn = 2
dynamicLagrangian = 3
DeardorffDiffStress = 4
WALE = 5
SpalartAllmarasDES = 6
SpalartAllmarasDDES = 7
SpalartAllmarasIDDES = 8
kOmegaSSTDES = 9
kOmegaSSTDDES = 10
kOmegaSSTIDDES = 11

# LES filters
SIMPLE_FILTER = 0
ANISOTROPIC_FILTER = 1
LAPLACE_FILTER = 2

# delta models
smooth = 0
Prandtl = 1
maxDeltaxyz = 2
cubeRootVol = 3
maxDeltaxyzCubeRoot = 4
vanDriest = 5
IDDESDelta = 6

# additional fields to write out during post-processing
Q = 0
VORTICITY = 1
LAMBDA_2 = 2
ENSTROPHY = 3

# initial conditions
BOUNDARY_CONDITIONED_BASED = 0
ZERO_VELOCITY = 1
CUSTOM = 2

# field type
SCALAR = 0
VECTOR = 1
TENSOR = 2