class WriteHeader:
    @staticmethod
    def get_header(version, class_name, location, object):
        return (
            f'/*--------------------------------*- C++ -*----------------------------------*\\\n'
            f'| =========                 |                                                 |\n'
            f'| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n'
            f'|  \\\    /   O peration     | Version:  {version}                                 |\n'
            f'|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |\n'
            f'|    \\\/     M anipulation  |                                                 |\n'
            f'|                                                                             |\n'
            f'| This file was automatically generated using the OpenFOAMCaseGenerator       |\n'
            f'| see https://github.com/tomrobin-teschner/OpenFOAMCaseGenerator              |\n'
            f'|                                                                             |\n'
            f'\*---------------------------------------------------------------------------*/\n'
            f'\n'
            f'FoamFile\n'
            f'{{\n'
            f'    version     2.0;\n'
            f'    format      ascii;\n'
            f'    class       {class_name};\n'
            f'    location    "{location}";\n'
            f'    object      {object};\n'
            f'}}\n'
            f'\n'
            f'// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'
            f'\n'
        )