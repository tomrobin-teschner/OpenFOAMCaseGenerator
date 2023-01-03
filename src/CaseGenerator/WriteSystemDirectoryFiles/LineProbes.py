from src.CaseGenerator.FileDirectoryIO import WriteHeader


class LineProbes:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        lines = WriteHeader.get_header(version, 'dictionary', 'system', 'sampling')

        lines += f'\n'
        for line in self.properties['line_probes']['location']:
            lines += f'{line["name"]}\n'
            lines += f'{{\n'
            lines += f'    type                  sets;\n'
            lines += f'    libs                  (sampling);\n'
            lines += f'\n'
            lines += f'    interpolationScheme   cellPoint;\n'
            lines += f'\n'
            lines += f'    setFormat             raw;\n'
            lines += f'\n'
            if self.properties['line_probes']['output_probe_at_every_timestep']:
                lines += f'    writeControl    timeStep;\n'
                lines += f'    writeInterval   1;\n'
            else:
                lines += f'    writeControl    writeTime;\n'
            lines += f'\n'
            lines += f'    log                   no;\n'
            lines += f'\n'
            lines += f'    sets\n'
            lines += f'    (\n'
            lines += f'        {line["name"]}\n'
            lines += f'        {{\n'
            lines += f'            type          uniform;\n'
            lines += f'            axis          xyz;\n'
            lines += f'            start         ({line["start"][0]} {line["start"][1]} {line["start"][2]});\n'
            lines += f'            end           ({line["end"][0]} {line["end"][1]} {line["end"][2]});\n'
            lines += f'            nPoints       {self.properties["line_probes"]["number_of_samples_on_line"]};\n'
            lines += f'        }}\n'
            lines += f'    );\n'
            lines += f'\n'
            lines += f'    fields\n'
            lines += f'    (\n'
            for variable in self.properties['line_probes']['variables_to_monitor']:
                lines += f'        {variable}\n'
            lines += f'    );\n'
            lines += f'}}\n'
            lines += f'\n'
        lines += f'// ************************************************************************* //\n'
        return lines
