from src.CaseGenerator.FileDirectoryIO import WriteHeader


class PointProbes:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        points = WriteHeader.get_header(version, 'dictionary', 'system', 'sampling')

        points += f'\n'
        points += f'point_probes\n'
        points += f'{{\n'
        points += f'    type            probes;\n'
        points += f'    libs            (fieldFunctionObjects);\n'
        points += f'\n'
        if self.properties['point_probes']['output_probe_at_every_timestep']:
            points += f'    writeControl    timeStep;\n'
            points += f'    writeInterval   1;\n'
        else:
            points += f'    writeControl    writeTime;\n'
        points += f'\n'
        points += f'    log             no;\n'
        points += f'\n'
        points += f'    probeLocations\n'
        points += f'    (\n'
        for point in self.properties['point_probes']['location']:
            points += f'        ({point[0]} {point[1]} {point[2]})\n'
        points += f'    );\n'
        points += f'\n'
        points += f'    fields\n'
        points += f'    (\n'
        for variable in self.properties['point_probes']['variables_to_monitor']:
            points += f'        {variable}\n'
        points += f'    );\n'
        points += f'}}\n'
        points += f'\n'
        points += f'// ************************************************************************* //\n'
        return points
