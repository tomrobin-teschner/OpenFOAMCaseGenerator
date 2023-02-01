from src.CaseGenerator.FileDirectoryIO import WriteHeader
from math import sin, cos, pi


class ForceCoefficients:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        RAD_TO_DEG = pi / 180
        tangential = self.properties['flow_properties']['axis_aligned_flow_direction']['tangential'].value
        normal = self.properties['flow_properties']['axis_aligned_flow_direction']['normal'].value
        aoa = self.properties['flow_properties']['axis_aligned_flow_direction']['angle_of_attack']
        cofr = self.properties['dimensionless_coefficients']['center_of_rotation']
        rho = self.properties['flow_properties']['dimensional_properties']['material_properties']['rho']
        vel_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        l_ref = self.properties['dimensionless_coefficients']['reference_length']
        a_ref = self.properties['dimensionless_coefficients']['reference_area']
        lift_dir = [0, 0, 0]
        drag_dir = [0, 0, 0]
        pitch_dir = [0, 0, 0]

        axes_indices = [0, 1, 2]
        lift_drag_axis = [tangential, normal]
        pitch_axis = list(set(axes_indices).difference(lift_drag_axis))
        assert len(pitch_axis) == 1, ('Tangential and normal direction can not be the same axis.' +
                                      'Check the axis_aligned_flow_direction input')
        pitch_dir[pitch_axis[0]] = 1

        lift_dir[tangential] = -sin(aoa * RAD_TO_DEG)
        lift_dir[normal] = cos(aoa * RAD_TO_DEG)

        drag_dir[tangential] = cos(aoa * RAD_TO_DEG)
        drag_dir[normal] = sin(aoa * RAD_TO_DEG)

        vector_to_string = lambda s: '(' + str(s[0]) + ' ' + str(s[1]) + ' ' + str(s[2]) + ')'
        lift_dir_str = vector_to_string(lift_dir)
        drag_dir_str = vector_to_string(drag_dir)
        pitch_dir_str = vector_to_string(pitch_dir)
        cofr_str = vector_to_string(cofr)

        version = self.properties['file_properties']['version']
        force_coef = WriteHeader.get_header(version, 'dictionary', 'system', 'forceCoefficiens')
        force_coef += f'\n'
        force_coef += f'forceCoeffs\n'
        force_coef += f'{{\n'
        force_coef += f'    type            forceCoeffs;\n'
        force_coef += f'\n'
        force_coef += f'    libs            (forces);\n'
        force_coef += f'\n'
        force_coef += f'    writeControl    timeStep;\n'
        force_coef += f'    timeInterval    1;\n'
        force_coef += f'\n'
        force_coef += f'    log             yes;\n'
        force_coef += f'\n'
        if len(self.properties['dimensionless_coefficients']['wall_boundaries']) == 1:
            wall_bc = self.properties['dimensionless_coefficients']['wall_boundaries'][0]
            force_coef += f'    patches         ({wall_bc});\n'
        else:
            force_coef += f'    patches         ('
            temp_str = ''
            for boundary in self.properties['dimensionless_coefficients']['wall_boundaries']:
                temp_str += boundary + ' '
            force_coef += f'{temp_str[:-1]});\n'
        force_coef += f'    rho             rhoInf;\n'
        force_coef += f'    rhoInf          {rho};\n'
        force_coef += f'    liftDir         {lift_dir_str};\n'
        force_coef += f'    dragDir         {drag_dir_str};\n'
        force_coef += f'    CofR            {cofr_str};\n'
        force_coef += f'    pitchAxis       {pitch_dir_str};\n'
        force_coef += f'    magUInf         {vel_mag};\n'
        force_coef += f'    lRef            {l_ref};\n'
        force_coef += f'    Aref            {a_ref};\n'
        force_coef += f'}}\n'
        force_coef += f'\n'
        force_coef += f'// ************************************************************************* //\n'
        return force_coef
