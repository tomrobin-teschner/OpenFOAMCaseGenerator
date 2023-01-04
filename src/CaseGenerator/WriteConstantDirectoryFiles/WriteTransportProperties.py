class TransportPropertiesFile:
    def __init__(self, properties):
        self.properties = properties
    
    def get_file_content(self):
        version = self.properties['file_properties']['version']
        nu = self.properties['flow_properties']['dimensional_properties']['nu']

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
            f'FoamFile\n'
            f'{{\n'
            f'    version     2.0;\n'
            f'    format      ascii;\n'
            f'    class       dictionary;\n'
            f'    location    "constant";\n'
            f'    object      transportProperties;\n'
            f'}}\n'
            f'// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'
            f'\n'
            f'transportModel  Newtonian;\n'
            f'\n'
            f'nu              {str(nu)};\n'
            f'\n'
            f'// ************************************************************************* //\n'
        )
