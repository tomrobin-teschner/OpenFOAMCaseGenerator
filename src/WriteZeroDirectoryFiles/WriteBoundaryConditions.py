from input import GlobalVariables as Parameters
from math import pow, sqrt
import copy


class WriteBoundaryConditions:
    def __init__(self, properties, file_manager):
        # assign private variables
        self.properties = properties
        self.file_manager = file_manager

        # list of all variables managed by this class. Each variable is mapped to a list of properties that contains
        # the following information
        #
        #   first index:    type of boundary field (either of scalar, vector or tensor type)
        #   second index:   dimension of of boundary field
        self.variables = {
            'U':        ['volVectorField',      '[0 1 -1 0 0 0 0]'],
            'p':        ['volScalarField',      '[0 2 -2 0 0 0 0]'],
            'T':        ['volScalarField',      '[0 0 0 1 0 0 0]'],
            'k':        ['volScalarField',      '[0 2 -2 0 0 0 0]'],
            'omega':    ['volScalarField',      '[0 0 -1 0 0 0 0]'],
            'epsilon':  ['volScalarField',      '[0 2 -3 0 0 0 0]'],
            'nuTilda':  ['volScalarField',      '[0 2 -1 0 0 0 0]'],
            'nut':      ['volScalarField',      '[0 2 -1 0 0 0 0]'],
            'alphat':   ['volScalarField',      '[1 -1 -1 0 0 0 0]'],
            'kt':       ['volScalarField',      '[0 2 -2 0 0 0 0]'],
            'kl':       ['volScalarField',      '[0 2 -2 0 0 0 0]'],
            'ReThetat': ['volScalarField',      '[0 0 0 0 0 0 0]'],
            'gammaInt': ['volScalarField',      '[0 0 0 0 0 0 0]'],
            'R':        ['volSymmTensorField',  '[0 2 -2 0 0 0 0]'],
        }

        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.variables['p'] = ['volScalarField',      '[1 -1 -2 0 0 0 0]']

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
        self.temperature = self.properties['flow_properties']['dimensional_properties']['T']
        self.turbulence_intensity = self.properties['turbulence_properties']['freestream_turbulent_intensity']
        self.freestream_k = self.__calculate_freestream_k()
        self.freestream_omega = self.__calculate_freestream_omega()
        self.freestream_epsilon = self.__calculate_freestream_epsilon()
        self.freestream_nuTilda = self.__calculate_freestream_nuTilda()
        self.freestream_ReThetat = self.__calculate_ReThetaT()

    def __calculate_turbulent_length_scale_for_internal_flows(self):
        return 0.07 * self.properties['dimensionless_coefficients']['reference_length']

    def __calculate_turbulent_length_scale_for_external_flows(self):
        Re = self.properties['flow_properties']['non_dimensional_properties']['reynolds_number']
        L = self.properties['dimensionless_coefficients']['reference_length']
        delta = 0.37 * L / pow(Re, 0.2)
        return 0.4 * delta

    def __calculate_turbulent_to_laminar_viscosity_ratio(self):
        TI = self.turbulence_intensity
        if TI < 0.01:
            return 1
        elif 0.01 <= TI < 0.05:
            return 1 + 9 * (TI - 0.01) / 0.04
        elif 0.05 <= TI < 0.1:
            return 10 + 90 * (TI - 0.05) / 0.05
        elif TI >= 0.1:
            return 100

    def __calculate_freestream_k(self):
        TI = self.turbulence_intensity
        UMag = self.velocity_magnitude
        return 1.5 * pow(UMag * TI, 2)

    def __calculate_freestream_omega(self):
        turbulence_at_inlet = self.properties['turbulence_properties']['turbulent_quantities_at_inlet']
        turbulent_length_scale = self.__calculate_turbulent_length_scale_for_internal_flows()
        turbulent_to_laminar_viscosity_ratio = self.properties['turbulence_properties']['turbulent_to_laminar_ratio']
        turbulent_to_laminar_viscosity_ratio_calculated = self.__calculate_turbulent_to_laminar_viscosity_ratio()
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        k = self.freestream_k

        if turbulence_at_inlet == Parameters.INTERNAL:
            return pow(Parameters.C_MU, -0.25) * pow(k, 0.5) / turbulent_length_scale
        elif turbulence_at_inlet == Parameters.EXTERNAL:
            return pow(Parameters.C_MU, -0.25) * pow(k, 0.5) / turbulent_length_scale
        elif turbulence_at_inlet == Parameters.RATIO:
            return (k / nu) / turbulent_to_laminar_viscosity_ratio
        elif turbulence_at_inlet == Parameters.RATIO_AUTO:
            return (k / nu) / turbulent_to_laminar_viscosity_ratio_calculated

    def __calculate_freestream_epsilon(self):
        turbulence_at_inlet = self.properties['turbulence_properties']['turbulent_quantities_at_inlet']
        turbulent_length_scale = self.__calculate_turbulent_length_scale_for_internal_flows()
        turbulent_to_laminar_viscosity_ratio = self.properties['turbulence_properties']['turbulent_to_laminar_ratio']
        turbulent_to_laminar_viscosity_ratio_calculated = self.__calculate_turbulent_to_laminar_viscosity_ratio()
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        k = self.freestream_k

        if turbulence_at_inlet == Parameters.INTERNAL:
            return pow(Parameters.C_MU, 0.75) * pow(k, 1.5) / turbulent_length_scale
        elif turbulence_at_inlet == Parameters.EXTERNAL:
            return pow(Parameters.C_MU, 0.75) * pow(k, 1.5) / turbulent_length_scale
        elif turbulence_at_inlet == Parameters.RATIO:
            return (Parameters.C_MU * pow(k, 2) / nu) / turbulent_to_laminar_viscosity_ratio
        elif turbulence_at_inlet == Parameters.RATIO_AUTO:
            return (Parameters.C_MU * pow(k, 2) / nu) / turbulent_to_laminar_viscosity_ratio_calculated

    def __calculate_freestream_nuTilda(self):
        turbulence_at_inlet = self.properties['turbulence_properties']['turbulent_quantities_at_inlet']
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        turbulent_length_scale = self.__calculate_turbulent_length_scale_for_internal_flows()
        k = self.freestream_k
        TI = self.turbulence_intensity
        UMag = self.velocity_magnitude

        if turbulence_at_inlet == Parameters.INTERNAL or turbulence_at_inlet == Parameters.EXTERNAL:
            return (sqrt(1.5) * UMag * TI * turbulent_length_scale)
        else:
            return 5 * nu

    def __calculate_ReThetaT(self):
        TI = self.turbulence_intensity
        if TI <= 0.013:
            return 1173.51 - 589.428 * TI * 100 + 0.2196 / pow(TI * 100, 2)
        elif TI > 0.013:
            return 331.5 / pow((TI * 100 - 0.5658), 0.671)

    def write_all_boundary_conditions(self):
        # open files
        file_id = self.__open_boundary_condition_files()

        # write headers
        self.__write_headers_to_file(file_id)

        # write dimensions
        self.__write_dimensions_to_file(file_id)

        # construct initial conditions
        bc_freestream_conditions, bc_zero_initial_conditions = self.__construct_initial_conditions()

        # write initial field
        self.__write_initial_conditions_to_file(file_id, bc_freestream_conditions, bc_zero_initial_conditions)

        # write boundary conditions here
        self.__write_boundary_condition_entries_to_file(file_id, bc_freestream_conditions)

        # close all boundary condition files
        self.__close_boundary_condition_files(file_id)

    def __open_boundary_condition_files(self):
        file_id = {}
        for var in self.variables:
            file_id[var] = self.file_manager.create_file('0', var)
        return file_id

    def __close_boundary_condition_files(self, file_id):
        for var in self.variables:
            self.file_manager.close_file(file_id[var])

    def __write_headers_to_file(self, file_id):
        for var, bc_props in self.variables.items():
            self.file_manager.write_header(file_id[var], bc_props[Parameters.BC_TYPE], '0', var)

    def __write_dimensions_to_file(self, file_id):
        for var, bc_props in self.variables.items():
            self.file_manager.write(file_id[var], '\ndimensions      ' + bc_props[Parameters.BC_DIMENSIONS] + ';\n\n')

    def __write_initial_conditions_to_file(self, file_id, bc_freestream_conditions, bc_zero_initial_conditions):
        initial_conditions_type = self.properties['flow_properties']['initial_conditions']
        custom_initial_conditions_flag = self.properties['flow_properties']['custom_initial_conditions']
        custom_initial_conditions_setup = self.properties['flow_properties']['custom_initial_conditions_setup']
        for var in self.variables:
            if custom_initial_conditions_flag:
                if var in custom_initial_conditions_setup:
                    path_to_script = custom_initial_conditions_setup[var]
                    self.__write_custom_initial_conditions(file_id[var], path_to_script)
            if (custom_initial_conditions_flag is False) or (var not in custom_initial_conditions_setup):
                if initial_conditions_type == Parameters.BOUNDARY_CONDITIONED_BASED:
                    self.file_manager.write(file_id[var], 'internalField   ' + bc_freestream_conditions[var] + ';\n\n')
                elif initial_conditions_type == Parameters.ZERO_VELOCITY:
                    self.file_manager.write(file_id[var],
                                            'internalField   ' + bc_zero_initial_conditions[var] + ';\n\n')

    def __construct_initial_conditions(self):
        U = self.properties['flow_properties']['dimensional_properties']['velocity_vector']
        uiui = (2.0 / 3.0) * self.freestream_k
        if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            p_initial = '0'
        elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            p_initial = str(self.properties['flow_properties']['dimensional_properties']['p'])
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
            'R': 'uniform (' + str(uiui) + ' 0 0 ' + str(uiui) + ' 0 ' + str(uiui) + ')'
        }

        bc_zero_initial_conditions = copy.deepcopy(bc_freestream_conditions)
        bc_zero_initial_conditions['U'] = 'uniform (0 0 0)'
        bc_zero_initial_conditions['nuTilda'] = 'uniform 0'
        bc_zero_initial_conditions['R'] = 'uniform (0 0 0 0 0 0)'

        return bc_freestream_conditions, bc_zero_initial_conditions

    def __write_boundary_condition_entries_to_file(self, file_id, bc_freestream_conditions):
        for var in self.variables:
            self.file_manager.write(file_id[var], 'boundaryField\n{\n')

        for name, bc_type in self.properties['boundary_properties']['boundary_conditions'].items():
            for var in self.variables:
                # write boundary condition's name
                self.file_manager.write(file_id[var], '    ' + name + '\n    {\n')

                # write inlet boundary conditions
                if bc_type == Parameters.INLET or bc_type == Parameters.DFSEM_INLET:
                    self.__inlet_boundary_condition(file_id, var, name, bc_type, bc_freestream_conditions)

                # write standard outlet boundary conditions
                if bc_type == Parameters.OUTLET:
                    self.__outlet_boundary_condition(bc_freestream_conditions, file_id, var)

                # write backflow outlet boundary conditions
                if bc_type == Parameters.BACKFLOW_OUTLET:
                    self.__backflow_boundary_condition(bc_freestream_conditions, file_id, var)

                # write advective outlet boundary conditions
                if bc_type == Parameters.ADVECTIVE_OUTLET:
                    self.__advective_boundary_condition(file_id, var)

                # wall boundary condition
                if bc_type == Parameters.WALL:
                    self._wall_boundary_condition(file_id, var, bc_freestream_conditions)

                # freestream boundary condition
                if bc_type == Parameters.FREESTREAM:
                    self.__freestream_boundary_condition(file_id, var, bc_freestream_conditions)

                # symmetry boundary condition
                if bc_type == Parameters.SYMMETRY:
                    self.__symmetry_boundary_condition(file_id, var)

                # cyclic boundary conditions
                if bc_type == Parameters.CYCLIC:
                    self.__cyclic_boundary_condition(file_id, var)

                # empty boundary conditions
                if bc_type == Parameters.EMPTY:
                    self.__empty_boundary_condition(file_id, var)

                # close boundary condition writing
                self.file_manager.write(file_id[var], '    }\n')

        for var in self.variables:
            self.file_manager.write(file_id[var], '}')

    def __inlet_boundary_condition(self, file_id, var, name, bc_type, bc_freestream_conditions):
        custom_inlet = self.properties['boundary_properties']['custom_inlet_boundary_conditions']
        custom_inlet_setup = self.properties['boundary_properties']['custom_inlet_boundary_conditions_setup']

        if custom_inlet:
            if var in custom_inlet_setup:
                path_to_script = custom_inlet_setup[var]
                self.__write_custom_inlet_profile(file_id[var], 8, path_to_script)
        if (custom_inlet is False) or (var not in custom_inlet_setup):
            if var == 'U':
                if bc_type == Parameters.INLET:
                    self.__dirichlet(file_id[var], bc_freestream_conditions[var])
                elif bc_type == Parameters.DFSEM_INLET:
                    self.__write_dfsem_inlet(file_id[var], name, bc_freestream_conditions[var])
            elif var == 'p' and self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
                self.__neumann(file_id[var])
            elif var == 'nut' or var == 'alphat':
                self.__zero_calculated(file_id[var])
            else:
                self.__dirichlet(file_id[var], bc_freestream_conditions[var])

    def __outlet_boundary_condition(self, bc_freestream_conditions, file_id, var):
        if var == 'p' and self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            self.__dirichlet(file_id[var], bc_freestream_conditions[var])
        elif var == 'nut' or var == 'alphat':
            self.__zero_calculated(file_id[var])
        else:
            self.__neumann(file_id[var])

    def __backflow_boundary_condition(self, bc_freestream_conditions, file_id, var):
        if var == 'p' and self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            self.__dirichlet(file_id[var], bc_freestream_conditions[var])
        elif var == 'nut' or var == 'alphat':
            self.__zero_calculated(file_id[var])
        else:
            self.__inlet_outlet(file_id[var], bc_freestream_conditions)

    def __advective_boundary_condition(self, file_id, var):
        self.__advective(file_id[var])

    def _wall_boundary_condition(self, file_id, var, bc_freestream_conditions):
        wall_modelling = self.properties['turbulence_properties']['wall_modelling']
        rans_model = self.properties['turbulence_properties']['RANS_model']
        write_wall_function_high_re = lambda v: self.__wall_function(file_id[v], bc_freestream_conditions[v],
                                                                     self.RANS_wall_functions[v][Parameters.HIGH_RE])
        write_wall_function_low_re = lambda v: self.__wall_function(file_id[v], bc_freestream_conditions[v],
                                                                    self.RANS_wall_functions[v][Parameters.LOW_RE])
        if var == 'U':
            self.__no_slip_wall(file_id[var])

        elif var == 'k':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                write_wall_function_low_re(var)

        elif var == 'omega':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                if rans_model == Parameters.kkLOmega:
                    self.__neumann(file_id[var])
                else:
                    write_wall_function_low_re(var)

        elif var == 'epsilon':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                self.__neumann(file_id[var])

        elif var == 'nuTilda':
            if wall_modelling == Parameters.HIGH_RE:
                self.__neumann(file_id[var])
            elif wall_modelling == Parameters.LOW_RE:
                nuTilda = self.properties['flow_properties']['dimensional_properties']['nu'] / 2
                self.__dirichlet(file_id[var], 'uniform ' + str(nuTilda))

        elif var == 'nut':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                write_wall_function_low_re(var)

        elif var == 'alphat':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                write_wall_function_low_re(var)

        elif var == 'kt':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                self.__dirichlet(file_id[var], bc_freestream_conditions[var])

        elif var == 'kl':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                self.__dirichlet(file_id[var], bc_freestream_conditions[var])

        elif var == 'R':
            if wall_modelling == Parameters.HIGH_RE:
                write_wall_function_high_re(var)
            elif wall_modelling == Parameters.LOW_RE:
                self.__dirichlet(file_id[var], 'uniform (0 0 0 0 0 0)')

        else:
            self.__neumann(file_id[var])

    def __freestream_boundary_condition(self, file_id, var, bc_freestream_conditions):
        if var == 'U':
            self.__freestream_velocity(file_id[var], bc_freestream_conditions[var])
        elif var == 'p':
            self.__freestream_pressure(file_id[var], bc_freestream_conditions[var])
        elif var == 'nut' or var == 'alphat':
            self.__zero_calculated(file_id[var])
        else:
            self.__freestream(file_id[var], bc_freestream_conditions[var])

    def __symmetry_boundary_condition(self, file_id, var):
        if var == 'nut' or var == 'alphat':
            self.__zero_calculated(file_id[var])
        else:
            self.__neumann(file_id[var])

    def __cyclic_boundary_condition(self, file_id, var):
        self.__periodic(file_id[var])

    def __empty_boundary_condition(self, file_id, var):
        self.__empty(file_id[var])

    def __dirichlet(self, file_id, initial_field):
        file_id.write('        type            fixedValue;\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __neumann(self, file_id):
        file_id.write('        type            zeroGradient;\n')

    def __no_slip_wall(self, file_id):
        file_id.write('        type            noSlip;\n')

    def __advective(self, file_id):
        file_id.write('        type            advective;\n')
        file_id.write('        phi             phi;\n')

    def __inlet_outlet(self, file_id, internal_field):
        file_id.write('        type            inletOutlet;\n')
        file_id.write('        inletValue      ' + internal_field + ';\n')

    def __periodic(self, file_id):
        file_id.write('        type            cyclic;\n')

    def __empty(self, file_id):
        file_id.write('        type            empty;\n')

    def __wall_function(self, file_id, initial_field, wall_function_type):
        file_id.write('        type            ' + wall_function_type + ';\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __zero_calculated(self, file_id):
        file_id.write('        type            calculated;\n')
        file_id.write('        value           uniform 0;\n')

    def __freestream_velocity(self, file_id, initial_field):
        file_id.write('        type            freestreamVelocity;\n')
        file_id.write('        freestreamValue ' + initial_field + ';\n')

    def __freestream_pressure(self, file_id, initial_field):
        file_id.write('        type            freestreamPressure;\n')
        file_id.write('        freestreamValue ' + initial_field + ';\n')

    def __freestream(self, file_id, initial_field):
        file_id.write('        type            freestream;\n')
        file_id.write('        freestreamValue ' + initial_field + ';\n')

    def __write_dfsem_inlet(self, file_id, bc_name, initial_field):
        custom_DFSEM_conditions = self.properties['boundary_properties']['custom_DFSEM_conditions']
        custom_DFSEM_conditions_setup = self.properties['boundary_properties']['custom_DFSEM_conditions_setup']
        length_scale = self.properties['dimensionless_coefficients']['reference_length']
        R = self.properties['boundary_properties']['reynolds_stresses']
        L = self.properties['boundary_properties']['turbulent_length_scale']
        nCellsPerEddy = self.properties['boundary_properties']['number_of_cells_per_eddy']

        init_reynolds_stresses = 'uniform (' + str(R[0]) + ' ' + str(R[1]) + ' ' + str(R[2]) + ' ' + str(R[3]) + ' '\
                                 + str(R[4]) + ' ' + str(R[5]) + ')'
        init_turbulent_length_scale = 'uniform ' + str(L)

        file_id.write('        type            turbulentDFSEMInlet;\n')
        file_id.write('        delta           ' + str(length_scale) + ';\n')

        if custom_DFSEM_conditions:
            if 'R' in custom_DFSEM_conditions_setup:
                file_id.write('        R\n        {\n')
                path_to_script = custom_DFSEM_conditions_setup['R']
                self.__write_custom_inlet_profile(file_id, 12, path_to_script)
                file_id.write('        }\n')
            if 'U' in custom_DFSEM_conditions_setup:
                file_id.write('        U\n        {\n')
                path_to_script = custom_DFSEM_conditions_setup['U']
                self.__write_custom_inlet_profile(file_id, 12, path_to_script)
                file_id.write('        }\n')
            if 'L' in custom_DFSEM_conditions_setup:
                file_id.write('        L\n        {\n')
                path_to_script = custom_DFSEM_conditions_setup['L']
                self.__write_custom_inlet_profile(file_id, 12, path_to_script)
                file_id.write('        }\n')

        if (custom_DFSEM_conditions is False) or ('R' not in custom_DFSEM_conditions_setup):
            file_id.write('        R               ' + init_reynolds_stresses + ';\n')

        if (custom_DFSEM_conditions is False) or ('U' not in custom_DFSEM_conditions_setup):
            file_id.write('        U               ' + initial_field + ';\n')

        if (custom_DFSEM_conditions is False) or ('L' not in custom_DFSEM_conditions_setup):
            if self.properties['boundary_properties']['set_turbulent_length_scale_at_inlet']:
                file_id.write('        L               ' + init_turbulent_length_scale + ';\n')
            else:
                file_id.write('        L               uniform 0;\n')
                file_id.write('        nCellsPerEddy   ' + str(nCellsPerEddy) + ';\n')

        file_id.write('        value           uniform (0 0 0);\n')

    def __write_custom_initial_conditions(self, file_id, path_to_script):
        file_id.write('internalField   #codeStream\n')
        file_id.write('{\n')
        file_id.write('    codeInclude\n')
        file_id.write('    #{\n')
        file_id.write('        #include "fvCFD.H"\n')
        file_id.write('    #};\n')
        file_id.write('\n')
        file_id.write('    codeOptions\n')
        file_id.write('    #{\n')
        file_id.write('        -I$(LIB_SRC)/finiteVolume/lnInclude \\\n')
        file_id.write('        -I$(LIB_SRC)/meshTools/lnInclude\n')
        file_id.write('    #};\n')
        file_id.write('\n')
        file_id.write('    codeLibs\n')
        file_id.write('    #{\n')
        file_id.write('        -lmeshTools \\\n')
        file_id.write('        -lfiniteVolume\n')
        file_id.write('    #};\n')
        file_id.write('\n')
        file_id.write('    code\n')
        file_id.write('    #{\n')

        custom_initial_condition_script = open(path_to_script, 'r')
        all_lines = custom_initial_condition_script.readlines()
        spaces = '        '
        for line in all_lines:
            file_id.write(spaces + line)

        file_id.write('\n')
        file_id.write('    #};\n')
        file_id.write('};\n')
        file_id.write('\n')

    def __write_custom_inlet_profile(self, file_id, leading_spaces, path_to_script):
        spaces = ' ' * leading_spaces
        file_id.write(spaces + '#codeStream\n')
        file_id.write(spaces + '{\n')
        file_id.write(spaces + '    codeInclude\n')
        file_id.write(spaces + '    #{\n')
        file_id.write(spaces + '        #include "fvCFD.H"\n')
        file_id.write(spaces + '    #};\n')
        file_id.write('\n')
        file_id.write(spaces + '    codeOptions\n')
        file_id.write(spaces + '    #{\n')
        file_id.write(spaces + '        -I$(LIB_SRC)/finiteVolume/lnInclude \\\n')
        file_id.write(spaces + '        -I$(LIB_SRC)/meshTools/lnInclude\n')
        file_id.write(spaces + '    #};\n')
        file_id.write('\n')
        file_id.write(spaces + '    codeLibs\n')
        file_id.write(spaces + '    #{\n')
        file_id.write(spaces + '        -lmeshTools \\\n')
        file_id.write(spaces + '        -lfiniteVolume\n')
        file_id.write(spaces + '    #};\n')
        file_id.write('\n')
        file_id.write(spaces + '    code\n')
        file_id.write(spaces + '    #{\n')

        custom_inlet_script = open(path_to_script, 'r')
        all_lines = custom_inlet_script.readlines()
        code_spaces = ' ' * 8
        for line in all_lines:
            file_id.write(spaces + code_spaces + line)

        file_id.write('\n')
        file_id.write(spaces + '    #};\n')
        file_id.write(spaces + '};\n')
