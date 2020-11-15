# boundary condition ID
INLET = 0
OUTLET = 1
WALL = 2
EMPTY = 3
SYMMETRY = 4
CYCLIC = 5

# outlet boundary condition ID
NEUMANN = 0
ADVECTIVE = 1
INLET_OUTLET = 2

# turbulence constant
C_MU = 0.09

# simulation type
LAMINAR = 0
RANS = 1
LES = 2

# wall modelling type
LOW_RE = 0
HIGH_RE = 1

# output write control
TIME_STEP = 0
RUN_TIME = 1
ADJUSTABLE_RUN_TIME = 2
CPU_TIME = 3
CLOCK_TIME = 4

# numerical schemes
STEADY_STATE = 0
FIRST_ORDER = 1
SECOND_ORDER = 2
THIRD_ORDER = 3

# stability controlling parameter for gradient schemes
NO_CORRECTION = 0
SLIGHT_CORRECTION = 1
MODERATE_CORRECTION = 2
FULL_CORRECTION = 3
