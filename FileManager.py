import os


def create_folder(path, case_name):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(os.path.join(path, '0')):
        os.makedirs(os.path.join(path, '0'))
    if not os.path.exists(os.path.join(path, 'constant')):
        os.makedirs(os.path.join(path, 'constant'))
    if not os.path.exists(os.path.join(path, 'system')):
        os.makedirs(os.path.join(path, 'system'))
    file_id = open(os.path.join(path, case_name + '.foam'), 'w')


def write_header(file_id, version, object, location, class_type):
    file_id.write('/*--------------------------------*- C++ -*----------------------------------*\\\n')
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
    file_id.write('    class       ' + class_type + ';\n')
    file_id.write('    location    "' + location + '";\n')
    file_id.write('    object      ' + object + ';\n')
    file_id.write('}\n')
    file_id.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n')