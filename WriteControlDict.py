import os
import FileManager as Header


def write_control_dict(case_name, version):
    file_id = open(os.path.join(case_name, 'system', 'controlDict'), "w")
    Header.write_header(file_id, version, 'controlDict', 'system', 'dictionary')
    file_id.write('\n')
    file_id.write('application      pimpleFoam;\n\n')
    file_id.write('startFrom        startTime;\n\n')
    file_id.write('startTime        0;\n\n')
    file_id.write('stopAt           endTime;\n\n')
    file_id.write('endTime          1000;\n\n')
    file_id.write('deltaT           0.1;\n\n')
    file_id.write('maxDeltaT        1;\n\n')
    file_id.write('adjustTimeStep   yes;\n\n')
    file_id.write('maxCo            1.0;\n\n')
    file_id.write('writeControl     timeStep;\n\n')
    file_id.write('writeInterval    10;\n\n')
    file_id.write('purgeWrite       0;\n\n')
    file_id.write('writeFormat      ascii;\n\n')
    file_id.write('writePrecision   6;\n\n')
    file_id.write('writeCompression off;\n\n')
    file_id.write('timeFormat      general;\n\n')
    file_id.write('timePrecision   6;\n\n')
    file_id.write('runTimeModifiable true;\n\n')
    file_id.write('// ************************************************************************* //\n')
    file_id.close()
