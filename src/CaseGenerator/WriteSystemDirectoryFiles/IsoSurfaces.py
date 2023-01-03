from src.CaseGenerator.FileDirectoryIO import WriteHeader


class IsoSurfaces:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        iso_surface = WriteHeader.get_header(version, 'dictionary', 'system', 'sampling')
        
        iso_surface += f'\n'
        for index in range(0, len(self.properties['iso_surfaces']['flow_variable'])):
            field = self.properties['iso_surfaces']['flow_variable'][index]
            value = self.properties['iso_surfaces']['iso_value'][index]

            iso_surface += f'isoSurface_{field}\n'
            iso_surface += f'{{\n'
            iso_surface += f'    type                  surfaces;\n'
            iso_surface += f'    libs                  (sampling);\n'
            iso_surface += f'\n'
            iso_surface += f'    interpolationScheme   cellPoint;\n'
            iso_surface += f'\n'
            iso_surface += f'    surfaceFormat         vtk;\n'
            iso_surface += f'\n'
            if self.properties['iso_surfaces']['output_iso_surfaces_at_every_timestep']:
                iso_surface += f'    writeControl          timeStep;\n'
                iso_surface += f'    writeInterval         1;\n'
            else:
                iso_surface += f'    writeControl          writeTime;\n'
            iso_surface += f'\n'
            iso_surface += f'    log                   no;\n'
            iso_surface += f'\n'
            iso_surface += f'    surfaces\n'
            iso_surface += f'    {{\n'
            iso_surface += f'        isoSurface_{field}\n'
            iso_surface += f'        {{\n'
            iso_surface += f'            type          isoSurface;\n'
            iso_surface += f'            isoField      {field};\n'
            iso_surface += f'            isoValue      {value};\n'
            iso_surface += f'            interpolate   true;\n'
            iso_surface += f'        }}\n'
            iso_surface += f'    }}\n'
            iso_surface += f'\n'
            iso_surface += f'    fields\n'
            iso_surface += f'    (\n'
            iso_surface += f'        {field}\n'
            for additional_field in self.properties['iso_surfaces']['additional_field_to_write']:
                iso_surface += f'        {additional_field}\n'
            iso_surface += f'    );\n'
            iso_surface += f'}}\n'
            iso_surface += f'\n'
        iso_surface += f'// ************************************************************************* //\n'
        return iso_surface
