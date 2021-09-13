from input import GlobalVariables as Parameters
from math import sin, cos, pi


class WriteForceCoefficients:
    def __init__(self, properties, file_manager):
        self.file_manager = file_manager
        self.properties = properties

    def write_force_coefficients(self):
        RAD_TO_DEG = pi / 180
        tangential = self.properties['flow_properties']['axis_aligned_flow_direction']['tangential']
        normal = self.properties['flow_properties']['axis_aligned_flow_direction']['normal']
        aoa = self.properties['flow_properties']['axis_aligned_flow_direction']['angle_of_attack']
        cofr = self.properties['dimensionless_coefficients']['center_of_rotation']
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

        file_id = self.file_manager.create_file('system/include', 'forceCoefficients')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'forceCoefficiens')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'forceCoeffs\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            forceCoeffs;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    libs            (forces);\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    writeControl    timeStep;\n')
        self.file_manager.write(file_id, '    timeInterval    1;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    log             yes;\n')
        self.file_manager.write(file_id, '\n')
        if len(self.properties['dimensionless_coefficients']['wall_boundaries']) == 1:
            self.file_manager.write(file_id, '    patches         (' +
                                    self.properties['dimensionless_coefficients']['wall_boundaries'][0] + ');\n')
        else:
            self.file_manager.write(file_id, '    patches         (')
            temp_str = ''
            for boundary in self.properties['dimensionless_coefficients']['wall_boundaries']:
                temp_str += boundary + ' '
            self.file_manager.write(file_id, temp_str[:-1] + ');\n')
        self.file_manager.write(file_id, '    rho             rhoInf;\n')
        rho = str(self.properties['flow_properties']['dimensional_properties']['rho'])
        self.file_manager.write(file_id, '    rhoInf          ' + rho + ';\n')
        self.file_manager.write(file_id, '    liftDir         ' + lift_dir_str + ';\n')
        self.file_manager.write(file_id, '    dragDir         ' + drag_dir_str + ';\n')
        self.file_manager.write(file_id, '    CofR            ' + cofr_str + ';\n')
        self.file_manager.write(file_id, '    pitchAxis       ' + pitch_dir_str + ';\n')
        self.file_manager.write(file_id, '    magUInf         ' +
                                str(self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'])
                                + ';\n')
        self.file_manager.write(file_id, '    lRef            ' +
                                str(self.properties['dimensionless_coefficients']['reference_length']) + ';\n')
        self.file_manager.write(file_id, '    Aref            ' +
                                str(self.properties['dimensionless_coefficients']['reference_area']) + ';\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
