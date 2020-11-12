import os
import GlobalVariables as Parameters


def write_turbulence_properties(case_name, version, simulation_type):
    file_id = open(os.path.join(case_name, 'constant', 'turbulenceProperties'), "w")
    file_id.write('/*--------------------------------*- C++ -*----------------------------------*\ \n')
    file_id.write('| =========                 |                                                 |\n')
    file_id.write('| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
    file_id.write('|  \\\    /   O peration     | Version:  ' + version + '                                 |\n')
    file_id.write('|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |\n')
    file_id.write('|    \\\/     M anipulation  |                                                 |\n')
    file_id.write('\*---------------------------------------------------------------------------*/\n')
    file_id.write('FoamFile\n')
    file_id.write('{\n')
    file_id.write('    version     2.0;\n')
    file_id.write('    format      ascii;\n')
    file_id.write('    class       dictionary;\n')
    file_id.write('    location    "constant";\n')
    file_id.write('    object      turbulenceProperties;\n')
    file_id.write('}\n')
    file_id.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')
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
