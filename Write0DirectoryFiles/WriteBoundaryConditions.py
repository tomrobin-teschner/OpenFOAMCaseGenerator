from math import sqrt, pow
import GlobalVariables as Parameters

from math import pow


class WriteBoundaryConditions:
    def __init__(self, file_manager, boundary_properties, flow_properties, solver_properties):
        # assign private variables
        self.file_manager = file_manager
        self.boundary_properties = boundary_properties
        self.flow_properties = flow_properties
        self.solver_properties = solver_properties

        # calculate freestream conditions
        #   see https://www.cfd-online.com/Wiki/Turbulence_free-stream_boundary_conditions as a reference
        self.velocity_magnitude = self.flow_properties['velocity_magnitude']
        self.freestream_k = self.__calculate_freestream_k()
        self.freestream_omega = self.__calculate_freestream_omega()
        self.freestream_epsilon = self.__calculate_freestream_epsilon()
        self.freestream_nuTilda = self.__calculate_freestream_nuTilda()
        self.freestream_ReThetat = self.__calculate_ReThetaT()

    def __calculate_turbulent_length_scale_for_internal_flows(self):
        return 0.07 * self.flow_properties['reference_length']

    def __calculate_turbulent_length_scale_for_external_flows(self):
        Re = self.flow_properties['reynolds_number']
        L = self.flow_properties['reference_length']
        delta = 0.37 * L / pow(Re, 0.2)
        return 0.4 * delta

    def __calculate_turbulent_to_laminar_viscosity_ratio(self):
        if self.flow_properties['freestream_turbulent_intensity'] < 0.01:
            return 1
        elif 0.01 <= self.flow_properties['freestream_turbulent_intensity'] < 0.05:
            return 1 + 9 * (self.flow_properties['freestream_turbulent_intensity'] - 0.01) / 0.04
        elif 0.05 <= self.flow_properties['freestream_turbulent_intensity'] < 0.1:
            return 10 + 90 * (self.flow_properties['freestream_turbulent_intensity'] - 0.05) / 0.05
        elif self.flow_properties['freestream_turbulent_intensity'] >= 0.1:
            return 100

    def __calculate_freestream_k(self):
        return 1.5 * pow(self.velocity_magnitude * self.flow_properties['freestream_turbulent_intensity'], 2)

    def __calculate_freestream_omega(self):
        if self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.INTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_internal_flows()
            return pow(Parameters.C_MU, -0.25) * pow(self.freestream_k, 0.5) / tls
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.EXTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_external_flows()
            return pow(Parameters.C_MU, -0.25) * pow(self.freestream_k, 0.5) / tls
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.RATIO:
            return ((self.freestream_k / self.flow_properties['nu']) /
                    self.solver_properties['turbulent_to_laminar_ratio'])
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.RATIO_AUTO:
            ttlr = self.__calculate_turbulent_to_laminar_viscosity_ratio()
            return (self.freestream_k / self.flow_properties['nu']) / ttlr

    def __calculate_freestream_epsilon(self):
        if self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.INTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_internal_flows()
            return pow(Parameters.C_MU, 0.75) * pow(self.freestream_k, 1.5) / tls
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.EXTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_external_flows()
            return pow(Parameters.C_MU, 0.75) * pow(self.freestream_k, 1.5) / tls
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.RATIO:
            return ((Parameters.C_MU * pow(self.freestream_k, 2) / self.flow_properties['nu']) /
                    self.solver_properties['turbulent_to_laminar_ratio'])
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.RATIO_AUTO:
            ttlr = self.__calculate_turbulent_to_laminar_viscosity_ratio()
            return (Parameters.C_MU * pow(self.freestream_k, 2) / self.flow_properties['nu']) / ttlr

    def __calculate_freestream_nuTilda(self):
        if self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.INTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_internal_flows()
            return 1.5 * self.velocity_magnitude * self.flow_properties['freestream_turbulent_intensity'] * tls
        elif self.solver_properties['turbulent_quantities_at_inlet'] == Parameters.EXTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_external_flows()
            return 1.5 * self.velocity_magnitude * self.flow_properties['freestream_turbulent_intensity'] * tls
        else:
            return 5 * self.flow_properties['nu']

    def __calculate_ReThetaT(self):
        if self.flow_properties['freestream_turbulent_intensity'] <= 0.013:
            return (1173.51 - 589.428 * self.flow_properties['freestream_turbulent_intensity'] * 100 +
                    0.2196 / pow(self.flow_properties['freestream_turbulent_intensity'] * 100, 2))
        elif self.flow_properties['freestream_turbulent_intensity'] > 0.013:
            return 331.5 / pow((self.flow_properties['freestream_turbulent_intensity'] * 100 - 0.5658), 0.671)

    def __write_header(self, file_id, field_type, folder, variable_name, dimensions, internal_field):
        # create new boundary file
        self.file_manager.write_header(file_id, field_type, folder, variable_name)

        # write dimensions and internal-field
        initial_field = internal_field
        self.file_manager.write(file_id, '\ndimensions      ' + dimensions + ';\n\n')
        self.file_manager.write(file_id, 'internalField   ' + internal_field + ';\n\n')

    def write_U(self):
        file_id = self.file_manager.create_file('0', 'U')

        initial_field = ('uniform (' + str(self.flow_properties['inlet_velocity'][0]) + ' ' +
                         str(self.flow_properties['inlet_velocity'][1]) + ' ' +
                         str(self.flow_properties['inlet_velocity'][2]) + ')')

        self.__write_header(file_id, 'volVectorField', '0', 'U', '[0 1 -1 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                self.__no_slip_wall(file_id)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream_velocity(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_p(self):
        file_id = self.file_manager.create_file('0', 'p')
        initial_field = 'uniform ' + str(0)
        self.__write_header(file_id, 'volScalarField', '0', 'p', '[0 2 -2 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream_pressure(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_k(self):
        file_id = self.file_manager.create_file('0', 'k')
        initial_field = 'uniform ' + str(self.freestream_k)
        self.__write_header(file_id, 'volScalarField', '0', 'k', '[0 2 -2 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                if self.solver_properties['wall_modelling'] == Parameters.LOW_RE:
                    self.__kLowReWallFunction(file_id, initial_field)
                elif self.solver_properties['wall_modelling'] == Parameters.HIGH_RE:
                    self.__kqRWallFunction(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_epsilon(self):
        file_id = self.file_manager.create_file('0', 'epsilon')
        initial_field = 'uniform ' + str(self.freestream_epsilon)
        self.__write_header(file_id, 'volScalarField', '0', 'epsilon', '[0 2 -3 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                if self.solver_properties['wall_modelling'] == Parameters.LOW_RE:
                    self.__neumann(file_id)
                elif self.solver_properties['wall_modelling'] == Parameters.HIGH_RE:
                    self.__epsilonWallFunction(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_omega(self):
        file_id = self.file_manager.create_file('0', 'omega')
        initial_field = 'uniform ' + str(self.freestream_omega)
        self.__write_header(file_id, 'volScalarField', '0', 'omega', '[0 0 -1 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                if self.solver_properties['wall_modelling'] == Parameters.LOW_RE:
                    self.__omegaWallFunction(file_id, initial_field)
                elif self.solver_properties['wall_modelling'] == Parameters.HIGH_RE:
                    self.__omegaWallFunction(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_nuTilda(self):
        file_id = self.file_manager.create_file('0', 'nuTilda')
        initial_field = 'uniform ' + str(self.freestream_nuTilda)
        self.__write_header(file_id, 'volScalarField', '0', 'nuTilda', '[0 2 -1 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                if self.solver_properties['wall_modelling'] == Parameters.LOW_RE:
                    self.__dirichlet(file_id, 'uniform ' + str(self.flow_properties['nu'] / 2))
                elif self.solver_properties['wall_modelling'] == Parameters.HIGH_RE:
                    self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_nut(self):
        file_id = self.file_manager.create_file('0', 'nut')
        initial_field = 'uniform ' + str(0)
        self.__write_header(file_id, 'volScalarField', '0', 'nut', '[0 2 -1 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                if self.solver_properties['wall_modelling'] == Parameters.LOW_RE:
                    self.__nutLowReWallFunction(file_id, initial_field)
                elif self.solver_properties['wall_modelling'] == Parameters.HIGH_RE:
                    self.__nutkWallFunction(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            else:
                self.__zeroCalculated(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_ReThetat(self):
        file_id = self.file_manager.create_file('0', 'ReThetat')
        initial_field = 'uniform ' + str(self.freestream_ReThetat)
        self.__write_header(file_id, 'volScalarField', '0', 'ReThetat', '[0 0 0 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            else:
                self.__neumann(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_gammaInt(self):
        file_id = self.file_manager.create_file('0', 'gammaInt')
        initial_field = 'uniform ' + str(1)
        self.__write_header(file_id, 'volScalarField', '0', 'gammaInt', '[0 0 0 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            else:
                self.__neumann(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_R(self):
        file_id = self.file_manager.create_file('0', 'R')
        uiui = (2.0/3.0)*self.freestream_k
        initial_field = 'uniform (' + str(uiui) + ' 0 0 ' + str(uiui) + ' 0 ' + str(uiui) + ')'
        self.__write_header(file_id, 'volSymmTensorField', '0', 'R', '[0 2 -2 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.boundary_properties:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.boundary_properties[key] == Parameters.WALL:
                if self.solver_properties['wall_modelling'] == Parameters.LOW_RE:
                    self.__dirichlet(file_id, 'uniform (0 0 0 0 0 0)')
                elif self.solver_properties['wall_modelling'] == Parameters.HIGH_RE:
                    self.__kqRWallFunction(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.boundary_properties[key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.boundary_properties[key] == Parameters.INLET:
                self.__dirichlet(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.boundary_properties[key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.boundary_properties[key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

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

    def __kqRWallFunction(self, file_id, initial_field):
        file_id.write('        type            kqRWallFunction;\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __epsilonWallFunction(self, file_id, initial_field):
        file_id.write('        type            epsilonWallFunction;\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __omegaWallFunction(self, file_id, initial_field):
        file_id.write('        type            omegaWallFunction;\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __nutkWallFunction(self, file_id, initial_field):
        file_id.write('        type            nutkWallFunction;\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __kLowReWallFunction(self, file_id, initial_field):
        file_id.write('        type            kLowReWallFunction;\n')
        file_id.write('        value           ' + initial_field + ';\n')


    def __nutLowReWallFunction(self, file_id, initial_field):
        file_id.write('        type            nutLowReWallFunction;\n')
        file_id.write('        value           ' + initial_field + ';\n')

    def __zeroCalculated(self, file_id):
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
