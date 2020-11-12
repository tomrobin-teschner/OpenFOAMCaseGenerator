import os
import GlobalVariables as Parameters
import WriteBoundaryConditions as Header
import BoundaryConditions as boundary_conditions
from math import sqrt, pow

def write_boundary_condition(BC, outlet_type, velocity, TKE_intensity, reference_length, wall_functions, case_name, version):

    # velocity magnitude
    velocity_magnitude = sqrt(pow(velocity[0], 2) + pow(velocity[1], 2) + pow(velocity[2], 2))

    # calculate freestream turbulent kinetic energy
    k = 1.5 * pow(velocity_magnitude * TKE_intensity, 2)

    # calculate freestream dissipation rate epsilon
    epsilon = pow(Parameters.C_MU, 0.75) * pow(k, 1.5) / reference_length

    # create new boundary file
    file_id = open(os.path.join(case_name, '0', 'epsilon'), 'w')

    # write header
    Header.write_boilerplate(file_id, version, 'epsilon', 'volScalarField')

    # write dimensions and internfield
    initial_field = 'uniform ' + str(epsilon)
    file_id.write('\ndimensions      [0 2 -3 0 0 0 0];\n\ninternalField   ' + initial_field + ';\n\n')

    # write boundary conditions
    file_id.write('boundaryField\n{\n')
    for key in BC:
        file_id.write('    ' + key + '\n    {\n')
        if BC[key] == Parameters.WALL:
            if wall_functions:
                boundary_conditions.omegaWallFunction(file_id, initial_field)
            else:
                boundary_conditions.neumann(file_id)
        elif BC[key] == Parameters.OUTLET:
            if outlet_type == Parameters.NEUMANN:
                boundary_conditions.neumann(file_id)
            elif outlet_type == Parameters.ADVECTIVE:
                boundary_conditions.advective(file_id)
            elif outlet_type == Parameters.INLET_OUTLET:
                boundary_conditions.inlet_outlet(file_id, initial_field)
        elif BC[key] == Parameters.SYMMETRY:
            boundary_conditions.neumann(file_id)
        elif BC[key] == Parameters.INLET:
            boundary_conditions.dirichlet(file_id, initial_field)
        elif BC[key] == Parameters.CYCLIC:
            boundary_conditions.periodic(file_id)
        elif BC[key] == Parameters.EMPTY:
            boundary_conditions.empty(file_id)
        file_id.write('    }\n')

    file_id.write('}')
    file_id.close()