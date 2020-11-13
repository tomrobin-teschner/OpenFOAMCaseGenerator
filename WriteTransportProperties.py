import os
import FileManager as Header


def write_transport_properties(case_name, version, nu):
    file_id = open(os.path.join(case_name, 'constant', 'transportProperties'), "w")
    Header.write_header(file_id, version, 'transportProperties', 'constant', 'dictionary')
    file_id.write('\n')
    file_id.write('transportModel  Newtonian;\n')
    file_id.write('\n')
    file_id.write('nu              ' + str(nu) + ';\n')
    file_id.write('\n')
    file_id.write('// ************************************************************************* //\n')
    file_id.close()
