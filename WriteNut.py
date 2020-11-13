import os
import GlobalVariables as Parameters
import FileManager as Header
import BoundaryConditions as boundary_conditions
from math import sqrt, pow

def write_boundary_condition(BC, outlet_type, velocity, TKE_intensity, reference_length, case_name, version):

    # create new boundary file
    file_id = open(os.path.join(case_name, '0', 'nut'), 'w')

    # write header
    Header.write_header(file_id, version, 'nut', '0', 'volScalarField')

    # write dimensions and internfield
    initial_field = 'uniform ' + str(0)
    file_id.write('\ndimensions      [0 2 -1 0 0 0 0];\n\ninternalField   ' + initial_field + ';\n\n')

    # write boundary conditions
    file_id.write('boundaryField\n{\n')
    for key in BC:
        file_id.write('    ' + key + '\n    {\n')
        if BC[key] == Parameters.WALL:
            boundary_conditions.nutUSpaldingWallFunction(file_id)
        elif BC[key] == Parameters.CYCLIC:
            boundary_conditions.periodic(file_id)
        elif BC[key] == Parameters.EMPTY:
            boundary_conditions.empty(file_id)
        else:
            boundary_conditions.zeroCalculated(file_id)
        file_id.write('    }\n')

    file_id.write('}')
    file_id.close()