import GlobalVariables as Parameters
import BoundaryConditions as BoundaryConditions


def write_boundary_condition(file_manager, boundary_properties, pressure):
    # create new boundary file
    file_id = file_manager.create_file('0', 'p')
    file_manager.write_header(file_id, 'volScalarField', '0', 'p')

    # write dimensions and internal-field
    initial_field = 'uniform ' + str(pressure)
    file_manager.write(file_id, '\ndimensions      [0 2 -2 0 0 0 0];\n\ninternalField   ' + initial_field + ';\n\n')

    # write boundary conditions
    file_manager.write(file_id, 'boundaryField\n{\n')
    for key in boundary_properties:
        file_manager.write(file_id, '    ' + key + '\n    {\n')
        if boundary_properties[key] == Parameters.WALL:
            BoundaryConditions.neumann(file_id)
        elif boundary_properties[key] == Parameters.OUTLET:
            if boundary_properties['outlet_type'] == Parameters.NEUMANN:
                BoundaryConditions.dirichlet(file_id, initial_field)
            elif boundary_properties['outlet_type'] == Parameters.ADVECTIVE:
                BoundaryConditions.advective(file_id)
            elif boundary_properties['outlet_type'] == Parameters.INLET_OUTLET:
                BoundaryConditions.dirichlet(file_id, initial_field)
        elif boundary_properties[key] == Parameters.SYMMETRY:
            BoundaryConditions.neumann(file_id)
        elif boundary_properties[key] == Parameters.INLET:
            BoundaryConditions.neumann(file_id)
        elif boundary_properties[key] == Parameters.CYCLIC:
            BoundaryConditions.periodic(file_id)
        elif boundary_properties[key] == Parameters.EMPTY:
            BoundaryConditions.empty(file_id)
        file_manager.write(file_id, '    }\n')

    file_manager.write(file_id, '}')
    file_id.close()
