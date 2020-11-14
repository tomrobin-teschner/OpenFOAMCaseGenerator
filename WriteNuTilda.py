import GlobalVariables as Parameters
import BoundaryConditions as BoundaryConditions
from math import sqrt, pow


def write_boundary_condition(file_manager, boundary_properties, outlet_type, flow_properties, wall_functions):

    # velocity magnitude
    velocity_magnitude = (sqrt(pow(flow_properties['inlet_velocity'][0], 2) +
                               pow(flow_properties['inlet_velocity'][1], 2) +
                               pow(flow_properties['inlet_velocity'][2], 2)))

    # nuTilda free-stream conditions
    nuTilda = 1.5 * velocity_magnitude * flow_properties['TKE_intensity'] * flow_properties['reference_length']

    # create new boundary file
    file_id = file_manager.create_file('0', 'nuTilda')
    file_manager.write_header(file_id, 'volScalarField', '0', 'nuTilda')

    # write dimensions and internal-field
    initial_field = 'uniform ' + str(nuTilda)
    file_manager.write(file_id, '\ndimensions      [0 2 -1 0 0 0 0];\n\ninternalField   ' + initial_field + ';\n\n')

    # write boundary conditions
    file_manager.write(file_id, 'boundaryField\n{\n')
    for key in boundary_properties:
        file_manager.write(file_id, '    ' + key + '\n    {\n')
        if boundary_properties[key] == Parameters.WALL:
            if wall_functions:
                BoundaryConditions.neumann(file_id)
            else:
                BoundaryConditions.dirichlet(file_id, initial_field)
        elif boundary_properties[key] == Parameters.OUTLET:
            if outlet_type == Parameters.NEUMANN:
                BoundaryConditions.neumann(file_id)
            elif outlet_type == Parameters.ADVECTIVE:
                BoundaryConditions.advective(file_id)
            elif outlet_type == Parameters.INLET_OUTLET:
                BoundaryConditions.inlet_outlet(file_id, initial_field)
        elif boundary_properties[key] == Parameters.SYMMETRY:
            BoundaryConditions.neumann(file_id)
        elif boundary_properties[key] == Parameters.INLET:
            BoundaryConditions.dirichlet(file_id, initial_field)
        elif boundary_properties[key] == Parameters.CYCLIC:
            BoundaryConditions.periodic(file_id)
        elif boundary_properties[key] == Parameters.EMPTY:
            BoundaryConditions.empty(file_id)
        file_manager.write(file_id, '    }\n')

    file_manager.write(file_id, '}')
    file_id.close()
