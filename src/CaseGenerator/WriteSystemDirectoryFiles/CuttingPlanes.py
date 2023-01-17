from src.CaseGenerator.FileDirectoryIO import WriteHeader


class CuttingPlanes:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        cut_planes = WriteHeader.get_header(version, 'dictionary', 'system', 'sampling')

        cut_planes += f'\n'
        for line in self.properties['cutting_planes']['location']:
            cut_planes += f'{line["name"]}\n'
            cut_planes += f'{{\n'
            cut_planes += f'    type                  surfaces;\n'
            cut_planes += f'    libs                  (sampling);\n'
            cut_planes += f'\n'
            cut_planes += f'    interpolationScheme   cellPoint;\n'
            cut_planes += f'\n'
            cut_planes += f'    surfaceFormat         vtk;\n'
            cut_planes += f'\n'
            if self.properties['cutting_planes']['output_cutting_plane_at_every_timestep']:
                cut_planes += f'    writeControl    timeStep;\n'
                cut_planes += f'    writeInterval   1;\n'
            else:
                cut_planes += f'    writeControl    writeTime;\n'
            cut_planes += f'\n'
            cut_planes += f'    log                   no;\n'
            cut_planes += f'\n'
            cut_planes += f'    surfaces\n'
            cut_planes += f'    {{\n'
            cut_planes += f'        {line["name"]}\n'
            cut_planes += f'        {{\n'
            cut_planes += f'            type          cuttingPlane;\n'
            cut_planes += f'            planeType     pointAndNormal;\n'
            cut_planes += f'            pointAndNormalDict\n'
            cut_planes += f'            {{\n'
            cut_planes += f'                point     ({line["origin"][0]} {line["origin"][1]} {line["origin"][2]});\n'
            cut_planes += f'                normal    ({line["normal"][0]} {line["normal"][1]} {line["normal"][2]});\n'
            cut_planes += f'            }}\n'
            cut_planes += f'            interpolate   true;\n'
            cut_planes += f'        }}\n'
            cut_planes += f'    }}\n'
            cut_planes += f'\n'
            cut_planes += f'    fields\n'
            cut_planes += f'    (\n'
            for variable in self.properties['cutting_planes']['variables_to_monitor']:
                cut_planes += f'        {variable}\n'
            cut_planes += f'    );\n'
            cut_planes += f'}}\n'
            cut_planes += f'\n'
        cut_planes += f'// ************************************************************************* //\n'
        return cut_planes
