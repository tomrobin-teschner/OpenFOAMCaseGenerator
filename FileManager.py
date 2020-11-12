import os


def create_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)
    if not os.path.exists(os.path.join(name, '0')):
        os.makedirs(os.path.join(name, '0'))
    if not os.path.exists(os.path.join(name, 'constant')):
        os.makedirs(os.path.join(name, 'constant'))
    if not os.path.exists(os.path.join(name, 'system')):
        os.makedirs(os.path.join(name, 'system'))


def write_boundary_condition_header(file_id, version, variable, type):
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
    file_id.write('    class       ' + type + ';\n')
    file_id.write('    location    "0";\n')
    file_id.write('    object      ' + variable + ';\n')
    file_id.write('}\n')
    file_id.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')