import os
import GlobalVariables as Parameters
import FileManager as Header


def write_turbulence_properties(case_name, version, simulation_type):
    file_id = open(os.path.join(case_name, 'constant', 'turbulenceProperties'), "w")
    Header.write_header(file_id, version, 'turbulenceProperties', 'constant', 'dictionary')
    file_id.write('\n')
    if simulation_type == Parameters.LAMINAR:
        file_id.write('simulationType laminar;\n')
    elif simulation_type == Parameters.RANS:
        file_id.write('simulationType RAS;\n')
    elif simulation_type == Parameters.LES:
        file_id.write('simulationType LES;\n')
    file_id.write('\n')
    if simulation_type != Parameters.LAMINAR:
        if simulation_type == Parameters.RANS:
            file_id.write('RAS\n{\n')
            file_id.write('    RASModel        kOmegaSST\n')
            file_id.write('\n')
            file_id.write('    turbulence      on\n')
            file_id.write('\n')
            file_id.write('    printCoeffs     on\n')

        elif simulation_type == Parameters.LES:
            file_id.write('LES\n{\n')
            file_id.write('\n')

    file_id.write('}\n\n')
    file_id.write('// ************************************************************************* //\n')
    file_id.close()
