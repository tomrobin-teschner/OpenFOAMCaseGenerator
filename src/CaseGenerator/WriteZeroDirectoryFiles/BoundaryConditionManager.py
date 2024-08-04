from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator.WriteZeroDirectoryFiles.TurbulentFreestreamConditions import TurbulenceFreestreamConditions
from src.CaseGenerator.WriteZeroDirectoryFiles.StateVariableManager import StateVariableManager
from src.CaseGenerator.FileDirectoryIO.WriteHeader import WriteHeader
import copy
from math import sqrt, pow


class BoundaryConditionManager:
    def __init__(self, properties):
        self.properties = properties
        turbulence_freestream_conditions = TurbulenceFreestreamConditions(properties)
        state_variable_manager = StateVariableManager(properties)
        self.variable_names = state_variable_manager.get_active_variable_names()
        self.variable_field_types = state_variable_manager.get_active_variable_field_types()
        self.variable_dimensions = state_variable_manager.get_active_variable_dimensions()

        # list of all wall function types used for RANS turbulence modelling. Not all wall modelling approaches have
        # wall functions applied and appropriate dirichlet or neumann boundary conditions are set here instead. These
        # are left blank in the list below.
        self.RANS_wall_functions = {
            'k':       ['kLowReWallFunction', 'kqRWallFunction'],
            'kl':      ['', 'kqRWallFunction'],
            'kt':      ['', 'kqRWallFunction'],
            'omega':   ['omegaWallFunction', 'omegaWallFunction'],
            'epsilon': ['', 'epsilonWallFunction'],
            'nut':     ['nutLowReWallFunction', 'nutkWallFunction'],
            'alphat':  ['compressible::alphatJayatillekeWallFunction', 'compressible::alphatJayatillekeWallFunction'],
            'R':       ['kLowReWallFunction', 'kqRWallFunction'],
        }

        # calculate freestream conditions
        # see https://www.cfd-online.com/Wiki/Turbulence_free-stream_boundary_conditions as a reference
        self.velocity_magnitude = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        self.temperature = self.properties['flow_properties']['dimensional_properties']['material_properties']['T']
        self.turbulence_intensity = self.properties['turbulence_properties']['freestream_turbulent_intensity']

        self.freestream_k = turbulence_freestream_conditions.calculate_freestream_k()
        self.freestream_omega = turbulence_freestream_conditions.calculate_freestream_omega()
        self.freestream_epsilon = turbulence_freestream_conditions.calculate_freestream_epsilon()
        self.freestream_nuTilda = turbulence_freestream_conditions.calculate_freestream_nuTilda()
        self.freestream_ReThetat = turbulence_freestream_conditions.calculate_ReThetaT()

    def get_all_boundary_conditions(self):
        # create list that contains all text that will be written for each variable's boundary condition
        content = []
        for variable in self.variable_names:
            content.append('')
        
        # write headers
        for index in range(0, len(self.variable_names)):
            content[index] += self.__get_headers(index)

        # write dimensions
        for index in range(0, len(self.variable_names)):
            content[index] += self.__get_dimensions(index)

        # construct and write initial conditions
        bc_freestream_conditions, bc_zero_initial_conditions = self.__construct_initial_conditions()
        for index in range(0, len(self.variable_names)):
            content[index] += self.__get_initial_conditions(self.variable_names[index], bc_freestream_conditions,
                bc_zero_initial_conditions)

        # write boundary conditions here
        for index in range(0, len(self.variable_names)):
            content[index] += self.__get_boundary_condition(self.variable_names[index], bc_freestream_conditions)

        # write bottom separator
        for index in range(0, len(self.variable_names)):
            content[index] += f'\n// ************************************************************************* //\n'

        return [self.variable_names, content]

    def __get_headers(self, index):
        version = self.properties['file_properties']['version']
        return WriteHeader.get_header(version, self.variable_field_types[index], '0', self.variable_names[index])

    def __get_dimensions(self, index):
        return f'dimensions      {self.variable_dimensions[index]};\n\n'

    def __get_initial_conditions(self, var, bc_freestream_conditions, bc_zero_initial_conditions):
        initial_conditions_type = self.properties['flow_properties']['initial_conditions']
        custom_initial_conditions_flag = self.properties['flow_properties']['custom_initial_conditions']
        custom_initial_conditions_setup = self.properties['flow_properties']['custom_initial_conditions_setup']

        if custom_initial_conditions_flag:
            if var in custom_initial_conditions_setup:
                path_to_script = custom_initial_conditions_setup[var]
                return self.__get_custom_initial_conditions(path_to_script)
        if (custom_initial_conditions_flag is False) or (var not in custom_initial_conditions_setup):
            if initial_conditions_type == InitialConditions.boundary_condition_based:
                return f'internalField   {bc_freestream_conditions[var]};\n\n'
            elif initial_conditions_type == InitialConditions.zero_velocity:
                return f'internalField   {bc_zero_initial_conditions[var]};\n\n'

    def __construct_initial_conditions(self):
        U = self.properties['flow_properties']['dimensional_properties']['velocity_vector']
        uiui = (2.0 / 3.0) * self.freestream_k
        if self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
            p_initial = '0'
        elif self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            p_initial = str(self.properties['flow_properties']['dimensional_properties']['material_properties']['p'])
        bc_freestream_conditions = {
            'U': 'uniform (' + str(U[0]) + ' ' + str(U[1]) + ' ' + str(U[2]) + ')',
            'p': 'uniform ' + p_initial,
            'T': 'uniform ' + str(self.temperature),
            'k': 'uniform ' + str(self.freestream_k),
            'kt': 'uniform ' + str(self.freestream_k),
            'kl': 'uniform 0',
            'nut': 'uniform 0',
            'alphat': 'uniform 0',
            'epsilon': 'uniform ' + str(self.freestream_epsilon),
            'omega': 'uniform ' + str(self.freestream_omega),
            'nuTilda': 'uniform ' + str(self.freestream_nuTilda),
            'ReThetat': 'uniform ' + str(self.freestream_ReThetat),
            'gammaInt': 'uniform 1',
            'R': 'uniform (' + str(uiui) + ' 0 0 ' + str(uiui) + ' 0 ' + str(uiui) + ')',
            'flm': 'uniform 1e-4',
            'fmm': 'uniform 1',
        }

        bc_zero_initial_conditions = copy.deepcopy(bc_freestream_conditions)
        bc_zero_initial_conditions['U'] = 'uniform (0 0 0)'
        bc_zero_initial_conditions['nuTilda'] = 'uniform 0'
        bc_zero_initial_conditions['R'] = 'uniform (0 0 0 0 0 0)'

        return bc_freestream_conditions, bc_zero_initial_conditions

    def __get_boundary_condition(self, var, bc_freestream_conditions):
        bc_string = 'boundaryField\n{\n'

        for name, bc_type in self.properties['boundary_properties']['boundary_conditions'].items():
            bc_string += f'    {name}\n    {{\n'
            # write inlet boundary conditions
            if bc_type == BoundaryConditions.inlet or bc_type == BoundaryConditions.dfsem_inlet:
                bc_string += self.__inlet_boundary_condition(var, name, bc_type, bc_freestream_conditions)

            # write standard outlet boundary conditions
            if bc_type == BoundaryConditions.outlet:
                bc_string += self.__outlet_boundary_condition(bc_freestream_conditions, var)

            # write backflow outlet boundary conditions
            if bc_type == BoundaryConditions.backflow_outlet:
                bc_string += self.__backflow_boundary_condition(bc_freestream_conditions, var)

            # write advective outlet boundary conditions
            if bc_type == BoundaryConditions.advective_outlet:
                bc_string += self.__advective_boundary_condition()

            # wall boundary condition
            if bc_type == BoundaryConditions.wall:
                bc_string += self._wall_boundary_condition(var, bc_freestream_conditions)

            # freestream boundary condition
            if bc_type == BoundaryConditions.freestream:
                bc_string += self.__freestream_boundary_condition(var, bc_freestream_conditions)

            # symmetry boundary condition
            if bc_type == BoundaryConditions.symmetry:
                bc_string += self.__symmetry_boundary_condition(var)

            # cyclic boundary conditions
            if bc_type == BoundaryConditions.cyclic:
                bc_string += self.__cyclic_boundary_condition()

            # empty boundary conditions
            if bc_type == BoundaryConditions.empty:
                bc_string += self.__empty_boundary_condition()

            bc_string += f'    }}\n'

        bc_string += '}\n'
        return bc_string

    def __inlet_boundary_condition(self, var, name, bc_type, bc_freestream_conditions):
        custom_inlet = self.properties['boundary_properties']['custom_inlet_boundary_conditions']
        custom_inlet_setup = self.properties['boundary_properties']['custom_inlet_boundary_conditions_setup']

        if custom_inlet:
            if var in custom_inlet_setup:
                path_to_script = custom_inlet_setup[var]
                bc_name = name + 'BC'
                init_value = 'uniform (0 0 0)'
                return self.__get_custom_inlet_profile(init_value, bc_name, 8, path_to_script)
        if (custom_inlet is False) or (var not in custom_inlet_setup):
            if var == 'U':
                if bc_type == BoundaryConditions.inlet:
                    return self.__dirichlet(bc_freestream_conditions[var])
                elif bc_type == BoundaryConditions.dfsem_inlet:
                    return self.__write_dfsem_inlet(name, bc_freestream_conditions[var])
            elif var == 'p' and self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
                return self.__neumann()
            elif var == 'nut' or var == 'alphat':
                return self.__zero_calculated()
            else:
                return self.__dirichlet(bc_freestream_conditions[var])

    def __outlet_boundary_condition(self, bc_freestream_conditions, var):
        if var == 'p' and self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
            return self.__dirichlet(bc_freestream_conditions[var])
        elif var == 'nut' or var == 'alphat':
            return self.__zero_calculated()
        else:
            return self.__neumann()

    def __backflow_boundary_condition(self, bc_freestream_conditions, var):
        if var == 'p' and self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
            return self.__dirichlet(bc_freestream_conditions[var])
        elif var == 'nut' or var == 'alphat':
            return self.__zero_calculated()
        else:
            return self.__inlet_outlet(bc_freestream_conditions[var])

    def __advective_boundary_condition(self):
        return self.__advective()

    def _wall_boundary_condition(self, var, bc_freestream_conditions):
        wall_modelling = self.properties['turbulence_properties']['wall_modelling']
        RansModel = self.properties['turbulence_properties']['RansModel']
        write_wall_function_high_re = lambda v: self.__wall_function(bc_freestream_conditions[v],
                                                                     self.RANS_wall_functions[v][WallModelling.high_re.value])
        write_wall_function_low_re = lambda v: self.__wall_function(bc_freestream_conditions[v],
                                                                    self.RANS_wall_functions[v][WallModelling.low_re.value])
        if var == 'U':
            return self.__no_slip_wall()

        elif var == 'k':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return write_wall_function_low_re(var)

        elif var == 'omega':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                if RansModel == RansModel.kkLOmega:
                    return self.__neumann()
                else:
                    return write_wall_function_low_re(var)

        elif var == 'epsilon':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return self.__neumann()

        elif var == 'nuTilda':
            if wall_modelling == WallModelling.high_re:
                return self.__neumann()
            elif wall_modelling == WallModelling.low_re:
                nuTilda = self.properties['flow_properties']['dimensional_properties']['material_properties']['nu'] / 2
                return self.__dirichlet(f'uniform {nuTilda}')

        elif var == 'nut':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return write_wall_function_low_re(var)

        elif var == 'alphat':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return write_wall_function_low_re(var)

        elif var == 'kt':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return self.__dirichlet(bc_freestream_conditions[var])

        elif var == 'kl':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return self.__dirichlet(bc_freestream_conditions[var])

        elif var == 'R':
            if wall_modelling == WallModelling.high_re:
                return write_wall_function_high_re(var)
            elif wall_modelling == WallModelling.low_re:
                return self.__dirichlet('uniform (0 0 0 0 0 0)')

        else:
            return self.__neumann()

    def __freestream_boundary_condition(self, var, bc_freestream_conditions):
        if var == 'U':
            return self.__freestream_velocity(bc_freestream_conditions[var])
        elif var == 'p':
            return self.__freestream_pressure(bc_freestream_conditions[var])
        elif var == 'nut' or var == 'alphat':
            return self.__zero_calculated()
        else:
            return self.__freestream(bc_freestream_conditions[var])

    def __symmetry_boundary_condition(self, var):
        if var == 'nut' or var == 'alphat':
            return self.__zero_calculated()
        else:
            return self.__neumann()

    def __cyclic_boundary_condition(self):
        return self.__periodic()

    def __empty_boundary_condition(self):
        return self.__empty()

    def __dirichlet(self, initial_field):
        return (
            f'        type            fixedValue;\n'
            f'        value           {initial_field};\n'
        )

    def __neumann(self):
        return f'        type            zeroGradient;\n'

    def __no_slip_wall(self):
        return f'        type            noSlip;\n'

    def __advective(self):
        return (
            f'        type            advective;\n'
            f'        phi             phi;\n'
        )

    def __inlet_outlet(self, initial_field):
        return (
            f'        type            inletOutlet;\n'
            f'        inletValue      {initial_field};\n'
        )

    def __periodic(self):
        return f'        type            cyclic;\n'

    def __empty(self):
        return f'        type            empty;\n'

    def __wall_function(self, initial_field, wall_function_type):
        return ( 
            f'        type            {wall_function_type};\n'
            f'        value           {initial_field};\n'
        )
    def __zero_calculated(self):
        return (
            f'        type            calculated;\n'
            f'        value           uniform 0;\n'
        )

    def __freestream_velocity(self, initial_field):
        return (
            f'        type            freestreamVelocity;\n'
            f'        freestreamValue {initial_field};\n'
        )

    def __freestream_pressure(self, initial_field):
        return (
            f'        type            freestreamPressure;\n'
            f'        freestreamValue {initial_field};\n'
        )

    def __freestream(self, initial_field):
        return (
            f'        type            freestream;\n'
            f'        freestreamValue {initial_field};\n'
        )

    # TODO: remove once DFSEM is removed
    def __write_dfsem_inlet(self, bc_name, initial_field):
        pass
        # custom_DFSEM_conditions = self.properties['boundary_properties']['custom_DFSEM_conditions']
        # custom_DFSEM_conditions_setup = self.properties['boundary_properties']['custom_DFSEM_conditions_setup']
        # length_scale = self.properties['dimensionless_coefficients']['reference_length']
        # R = self.properties['boundary_properties']['reynolds_stresses']
        # L = self.properties['boundary_properties']['turbulent_length_scale']
        # nCellsPerEddy = self.properties['boundary_properties']['number_of_cells_per_eddy']

        # init_reynolds_stresses = 'uniform (' + str(R[0]) + ' ' + str(R[1]) + ' ' + str(R[2]) + ' ' + str(R[3]) + ' '\
        #                          + str(R[4]) + ' ' + str(R[5]) + ')'
        # init_turbulent_length_scale = 'uniform ' + str(L)

        # file_id.write('        type            turbulentDFSEMInlet;\n')
        # file_id.write('        delta           ' + str(length_scale) + ';\n')

        # if custom_DFSEM_conditions:
        #     if 'R' in custom_DFSEM_conditions_setup:
        #         file_id.write('        R\n        {\n')
        #         path_to_script = custom_DFSEM_conditions_setup['R']
        #         self.__write_custom_inlet_profile(file_id, init_reynolds_stresses, 'RBC', 12, path_to_script)
        #         file_id.write('        }\n')
        #     if 'U' in custom_DFSEM_conditions_setup:
        #         file_id.write('        U\n        {\n')
        #         path_to_script = custom_DFSEM_conditions_setup['U']
        #         init_value = 'uniform (0 0 0)'
        #         self.__write_custom_inlet_profile(file_id, init_value, 'UBC', 12, path_to_script)
        #         file_id.write('        }\n')
        #     if 'L' in custom_DFSEM_conditions_setup:
        #         file_id.write('        L\n        {\n')
        #         path_to_script = custom_DFSEM_conditions_setup['L']
        #         self.__write_custom_inlet_profile(file_id, init_turbulent_length_scale, 'LBC', 12, path_to_script)
        #         file_id.write('        }\n')

        # if (custom_DFSEM_conditions is False) or ('R' not in custom_DFSEM_conditions_setup):
        #     file_id.write('        R               ' + init_reynolds_stresses + ';\n')

        # if (custom_DFSEM_conditions is False) or ('U' not in custom_DFSEM_conditions_setup):
        #     file_id.write('        U               ' + initial_field + ';\n')

        # if (custom_DFSEM_conditions is False) or ('L' not in custom_DFSEM_conditions_setup):
        #     if self.properties['boundary_properties']['set_turbulent_length_scale_at_inlet']:
        #         file_id.write('        L               ' + init_turbulent_length_scale + ';\n')
        #     else:
        #         file_id.write('        L               uniform 0;\n')
        #         file_id.write('        nCellsPerEddy   ' + str(nCellsPerEddy) + ';\n')

        # file_id.write('        value           uniform (0 0 0);\n')

    def __get_custom_initial_conditions(self, path_to_script):
        custom_initial_condition_script = open(path_to_script, 'r')
        all_lines = custom_initial_condition_script.readlines()
        spaces = ' ' * 8
        code = ''
        for line in all_lines:
            code += spaces + line

        return (
            f'internalField   #codeStream\n'
            f'{{\n'
            f'    codeInclude\n'
            f'    #{{\n'
            f'        #include "fvCFD.H"\n'
            f'    #}};\n'
            f'\n'
            f'    codeOptions\n'
            f'    #{{\n'
            f'        -I$(LIB_SRC)/finiteVolume/lnInclude \\\n'
            f'        -I$(LIB_SRC)/meshTools/lnInclude\n'
            f'    #}};\n'
            f'\n'
            f'    codeLibs\n'
            f'    #{{\n'
            f'        -lmeshTools \\\n'
            f'        -lfiniteVolume\n'
            f'    #}};\n'
            f'\n'
            f'    code\n'
            f'    #{{\n'
            f'{code}'
            f'\n'
            f'    #}};\n'
            f'}};\n'
            f'\n'
        )

    def __get_custom_inlet_profile(self, init_value, bc_name, leading_spaces, path_to_script):
        spaces = ' ' * leading_spaces
        custom_inlet_script = open(path_to_script, 'r')
        all_lines = custom_inlet_script.readlines()
        code_spaces = ' ' * 8
        code = ''
        for line in all_lines:
            code += spaces + code_spaces + line
        
        return (
            f'{spaces}type    codedFixedValue;\n'
            f'{spaces}value   {init_value};\n'
            f'{spaces}name    {bc_name};\n'
            f'\n'
            f'{spaces}codeInclude\n'
            f'{spaces}#{{\n'
            f'{spaces}    #include "fvCFD.H"\n'
            f'{spaces}#}};\n'
            f'\n'
            f'{spaces}codeOptions\n'
            f'{spaces}#{{\n'
            f'{spaces}    -I$(LIB_SRC)/finiteVolume/lnInclude \\\n'
            f'{spaces}    -I$(LIB_SRC)/meshTools/lnInclude\n'
            f'{spaces}#}};\n'
            f'\n'
            f'{spaces}codeLibs\n'
            f'{spaces}#{{\n'
            f'{spaces}    -lmeshTools \\\n'
            f'{spaces}    -lfiniteVolume\n'
            f'{spaces}#}};\n'
            f'\n'
            f'{spaces}code\n'
            f'{spaces}#{{\n'
            f'{code}'  
            f'\n'
            f'{spaces}#}};\n'
        )

    def __write_custom_inlet_profile(self, file_id, init_value, bc_name, leading_spaces, path_to_script):
        spaces = ' ' * leading_spaces
        file_id.write(spaces + 'type    codedFixedValue;\n')
        file_id.write(spaces + 'value   ' + init_value + ';\n')
        file_id.write(spaces + 'name    ' + bc_name + ';\n')
        file_id.write('\n')
        file_id.write(spaces + 'codeInclude\n')
        file_id.write(spaces + '#{\n')
        file_id.write(spaces + '    #include "fvCFD.H"\n')
        file_id.write(spaces + '#};\n')
        file_id.write('\n')
        file_id.write(spaces + 'codeOptions\n')
        file_id.write(spaces + '#{\n')
        file_id.write(spaces + '    -I$(LIB_SRC)/finiteVolume/lnInclude \\\n')
        file_id.write(spaces + '    -I$(LIB_SRC)/meshTools/lnInclude\n')
        file_id.write(spaces + '#};\n')
        file_id.write('\n')
        file_id.write(spaces + 'codeLibs\n')
        file_id.write(spaces + '#{\n')
        file_id.write(spaces + '    -lmeshTools \\\n')
        file_id.write(spaces + '    -lfiniteVolume\n')
        file_id.write(spaces + '#};\n')
        file_id.write('\n')
        file_id.write(spaces + 'code\n')
        file_id.write(spaces + '#{\n')

        custom_inlet_script = open(path_to_script, 'r')
        all_lines = custom_inlet_script.readlines()
        code_spaces = ' ' * 8
        for line in all_lines:
            file_id.write(spaces + code_spaces + line)

        file_id.write('\n')
        file_id.write(spaces + '#};\n')
