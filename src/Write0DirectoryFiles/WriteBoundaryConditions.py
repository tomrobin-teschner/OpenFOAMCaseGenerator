from src import GlobalVariables as Parameters

import sys
from math import pow


class WriteBoundaryConditions:
    def __init__(self, properties, file_manager):
        # assign private variables
        self.properties = properties
        self.file_manager = file_manager

        # calculate freestream conditions
        # see https://www.cfd-online.com/Wiki/Turbulence_free-stream_boundary_conditions as a reference
        self.velocity_magnitude = self.properties['flow_properties']['velocity_magnitude']
        self.freestream_k = self.__calculate_freestream_k()
        self.freestream_omega = self.__calculate_freestream_omega()
        self.freestream_epsilon = self.__calculate_freestream_epsilon()
        self.freestream_nuTilda = self.__calculate_freestream_nuTilda()
        self.freestream_ReThetat = self.__calculate_ReThetaT()

    def __calculate_turbulent_length_scale_for_internal_flows(self):
        return 0.07 * self.properties['flow_properties']['reference_length']

    def __calculate_turbulent_length_scale_for_external_flows(self):
        Re = self.properties['flow_properties']['reynolds_number']
        L = self.properties['flow_properties']['reference_length']
        delta = 0.37 * L / pow(Re, 0.2)
        return 0.4 * delta

    def __calculate_turbulent_to_laminar_viscosity_ratio(self):
        if self.properties['flow_properties']['freestream_turbulent_intensity'] < 0.01:
            return 1
        elif 0.01 <= self.properties['flow_properties']['freestream_turbulent_intensity'] < 0.05:
            return 1 + 9 * (self.properties['flow_properties']['freestream_turbulent_intensity'] - 0.01) / 0.04
        elif 0.05 <= self.properties['flow_properties']['freestream_turbulent_intensity'] < 0.1:
            return 10 + 90 * (self.properties['flow_properties']['freestream_turbulent_intensity'] - 0.05) / 0.05
        elif self.properties['flow_properties']['freestream_turbulent_intensity'] >= 0.1:
            return 100

    def __calculate_freestream_k(self):
        return (1.5 * pow(self.velocity_magnitude *
                          self.properties['flow_properties']['freestream_turbulent_intensity'], 2))

    def __calculate_freestream_omega(self):
        if self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.INTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_internal_flows()
            return pow(Parameters.C_MU, -0.25) * pow(self.freestream_k, 0.5) / tls
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.EXTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_external_flows()
            return pow(Parameters.C_MU, -0.25) * pow(self.freestream_k, 0.5) / tls
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.RATIO:
            return ((self.freestream_k / self.properties['flow_properties']['nu']) /
                    self.properties['turbulence_properties']['turbulent_to_laminar_ratio'])
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.RATIO_AUTO:
            ttlr = self.__calculate_turbulent_to_laminar_viscosity_ratio()
            return (self.freestream_k / self.properties['flow_properties']['nu']) / ttlr

    def __calculate_freestream_epsilon(self):
        if self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.INTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_internal_flows()
            return pow(Parameters.C_MU, 0.75) * pow(self.freestream_k, 1.5) / tls
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.EXTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_external_flows()
            return pow(Parameters.C_MU, 0.75) * pow(self.freestream_k, 1.5) / tls
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.RATIO:
            return ((Parameters.C_MU * pow(self.freestream_k, 2) / self.properties['flow_properties']['nu']) /
                    self.properties['turbulence_properties']['turbulent_to_laminar_ratio'])
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.RATIO_AUTO:
            ttlr = self.__calculate_turbulent_to_laminar_viscosity_ratio()
            return (Parameters.C_MU * pow(self.freestream_k, 2) / self.properties['flow_properties']['nu']) / ttlr

    def __calculate_freestream_nuTilda(self):
        if self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.INTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_internal_flows()
            return (1.5 * self.velocity_magnitude *
                    self.properties['flow_properties']['freestream_turbulent_intensity'] * tls)
        elif self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] == Parameters.EXTERNAL:
            tls = self.__calculate_turbulent_length_scale_for_external_flows()
            return (1.5 * self.velocity_magnitude *
                    self.properties['flow_properties']['freestream_turbulent_intensity'] * tls)
        else:
            return 5 * self.properties['flow_properties']['nu']

    def __calculate_ReThetaT(self):
        if self.properties['flow_properties']['freestream_turbulent_intensity'] <= 0.013:
            return (1173.51 - 589.428 * self.properties['flow_properties']['freestream_turbulent_intensity'] * 100 +
                    0.2196 / pow(self.properties['flow_properties']['freestream_turbulent_intensity'] * 100, 2))
        elif self.properties['flow_properties']['freestream_turbulent_intensity'] > 0.013:
            return (331.5 / pow((self.properties['flow_properties']['freestream_turbulent_intensity'] * 100 - 0.5658),
                                0.671))

    def __write_header(self, file_id, field_type, folder, variable_name, dimensions, internal_field):
        # create new boundary file
        self.file_manager.write_header(file_id, field_type, folder, variable_name)

        # write dimensions and internal-field
        self.file_manager.write(file_id, '\ndimensions      ' + dimensions + ';\n\n')
        self.file_manager.write(file_id, 'internalField   ' + internal_field + ';\n\n')

    def write_all_appropriate_boundary_conditions(self):
        self.write_U()
        self.write_p()
        self.write_k()
        self.write_kt()
        self.write_kl()
        self.write_nut()
        self.write_omega()
        self.write_epsilon()
        self.write_nuTilda()
        self.write_ReThetat()
        self.write_gammaInt()
        self.write_R()

    def write_U(self):
        file_id = self.file_manager.create_file('0', 'U')

        initial_field = ('uniform (' + str(self.properties['flow_properties']['inlet_velocity'][0]) + ' ' +
                         str(self.properties['flow_properties']['inlet_velocity'][1]) + ' ' +
                         str(self.properties['flow_properties']['inlet_velocity'][2]) + ')')

        self.file_manager.write_header(file_id, 'volVectorField', '0', 'U')
        self.file_manager.write(file_id, '\ndimensions      [0 1 -1 0 0 0 0];\n\n')

        if self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if 'U' in self.properties['flow_properties']['custom_initial_conditions']['variables']:
                self.__custom_initial_conditions(file_id, Parameters.VECTOR)
            else:
                if (self.properties['flow_properties']['custom_initial_conditions']
                        ['non_custom_initialised_variables_treatment'] == Parameters.BOUNDARY_CONDITIONED_BASED):
                    self.file_manager.write(file_id, 'internalField   ' + initial_field + ';\n\n')
                elif (self.properties['flow_properties']['custom_initial_conditions']
                        ['non_custom_initialised_variables_treatment'] == Parameters.ZERO_VELOCITY):
                    self.file_manager.write(file_id, 'internalField   uniform (0 0 0);\n\n')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.BOUNDARY_CONDITIONED_BASED:
            self.file_manager.write(file_id, 'internalField   ' + initial_field + ';\n\n')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.ZERO_VELOCITY:
            self.file_manager.write(file_id, 'internalField   uniform (0 0 0);\n\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                self.__no_slip_wall(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.INLET:
                if self.properties['flow_properties']['custom_velocity_inlet_profile']:
                    self.file_manager.write(file_id, '        type            fixedValue;\n')
                    self.file_manager.write(file_id, '        value           ')
                    self.__custom_inlet_profile(file_id, key, Parameters.VECTOR)
                else:
                    self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET:
                self.__write_dfsem_inlet(file_id, key, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream_velocity(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_p(self):
        file_id = self.file_manager.create_file('0', 'p')
        initial_field = 'uniform ' + str(0)

        self.file_manager.write_header(file_id, 'volScalarField', '0', 'p')
        self.file_manager.write(file_id, '\ndimensions      [0 2 -2 0 0 0 0];\n\n')

        if self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if 'p' in self.properties['flow_properties']['custom_initial_conditions']['variables']:
                self.__custom_initial_conditions(file_id, Parameters.SCALAR)
            else:
                self.file_manager.write(file_id, 'internalField   ' + initial_field + ';\n\n')
        else:
            self.file_manager.write(file_id, 'internalField   ' + initial_field + ';\n\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                    self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream_pressure(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_k(self):
        file_id = self.file_manager.create_file('0', 'k')
        initial_field = 'uniform ' + str(self.freestream_k)

        if self.properties['flow_properties']['initial_conditions'] == Parameters.BOUNDARY_CONDITIONED_BASED:
            self.__write_header(file_id, 'volScalarField', '0', 'k', '[0 2 -2 0 0 0 0]', initial_field)
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.ZERO_VELOCITY:
            self.__write_header(file_id, 'volScalarField', '0', 'k', '[0 2 -2 0 0 0 0]', 'uniform 0')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.BOUNDARY_CONDITIONED_BASED):
                self.__write_header(file_id, 'volScalarField', '0', 'k', '[0 2 -2 0 0 0 0]', initial_field)
            elif (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.ZERO_VELOCITY):
                self.__write_header(file_id, 'volScalarField', '0', 'k', '[0 2 -2 0 0 0 0]', 'uniform 0')
            else:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nInitial condition for k not recognised. Use either BOUNDARY_CONDITIONED_BASED\n' +
                         'or ZERO_VELOCITY and restart the solver.\n' +
                         '\n=================================== END ERROR ===================================\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__kLowReWallFunction(file_id, initial_field)
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__kqRWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                    self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_kt(self):
        file_id = self.file_manager.create_file('0', 'kt')
        initial_field = 'uniform ' + str(self.freestream_k)

        if self.properties['flow_properties']['initial_conditions'] == Parameters.BOUNDARY_CONDITIONED_BASED:
            self.__write_header(file_id, 'volScalarField', '0', 'kt', '[0 2 -2 0 0 0 0]', initial_field)
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.ZERO_VELOCITY:
            self.__write_header(file_id, 'volScalarField', '0', 'kt', '[0 2 -2 0 0 0 0]', 'uniform 0')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.BOUNDARY_CONDITIONED_BASED):
                self.__write_header(file_id, 'volScalarField', '0', 'kt', '[0 2 -2 0 0 0 0]', initial_field)
            elif (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.ZERO_VELOCITY):
                self.__write_header(file_id, 'volScalarField', '0', 'kt', '[0 2 -2 0 0 0 0]', 'uniform 0')
            else:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nInitial condition for kt not recognised. Use either BOUNDARY_CONDITIONED_BASED\n' +
                         'or ZERO_VELOCITY and restart the solver.\n' +
                         '\n=================================== END ERROR ===================================\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__dirichlet(file_id, initial_field)
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__kqRWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_kl(self):
        file_id = self.file_manager.create_file('0', 'kl')
        initial_field = 'uniform 0'

        self.__write_header(file_id, 'volScalarField', '0', 'kl', '[0 2 -2 0 0 0 0]', initial_field)

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__dirichlet(file_id, initial_field)
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__kqRWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_epsilon(self):
        file_id = self.file_manager.create_file('0', 'epsilon')
        initial_field = 'uniform ' + str(self.freestream_epsilon)

        if self.properties['flow_properties']['initial_conditions'] == Parameters.BOUNDARY_CONDITIONED_BASED:
            self.__write_header(file_id, 'volScalarField', '0', 'epsilon', '[0 2 -3 0 0 0 0]', initial_field)
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.ZERO_VELOCITY:
            self.__write_header(file_id, 'volScalarField', '0', 'epsilon', '[0 2 -3 0 0 0 0]', 'uniform 0')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.BOUNDARY_CONDITIONED_BASED):
                self.__write_header(file_id, 'volScalarField', '0', 'epsilon', '[0 2 -3 0 0 0 0]', initial_field)
            elif (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.ZERO_VELOCITY):
                self.__write_header(file_id, 'volScalarField', '0', 'epsilon', '[0 2 -3 0 0 0 0]', 'uniform 0')
            else:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nInitial condition for epsilon not recognised. Use either\n' +
                         'BOUNDARY_CONDITIONED_BASED or ZERO_VELOCITY and restart the solver.\n' +
                         '\n=================================== END ERROR ===================================\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__neumann(file_id)
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__epsilonWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_omega(self):
        file_id = self.file_manager.create_file('0', 'omega')
        initial_field = 'uniform ' + str(self.freestream_omega)

        self.__write_header(file_id, 'volScalarField', '0', 'omega', '[0 0 -1 0 0 0 0]', initial_field)

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    if self.properties['turbulence_properties']['RANS_model'] == Parameters.kkLOmega:
                        self.__neumann(file_id)
                    else:
                        self.__omegaWallFunction(file_id, initial_field)
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__omegaWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_nuTilda(self):
        file_id = self.file_manager.create_file('0', 'nuTilda')
        initial_field = 'uniform ' + str(self.freestream_nuTilda)

        if self.properties['flow_properties']['initial_conditions'] == Parameters.BOUNDARY_CONDITIONED_BASED:
            self.__write_header(file_id, 'volScalarField', '0', 'nuTilda', '[0 2 -1 0 0 0 0]', initial_field)
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.ZERO_VELOCITY:
            self.__write_header(file_id, 'volScalarField', '0', 'nuTilda', '[0 2 -1 0 0 0 0]', 'uniform 0')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.BOUNDARY_CONDITIONED_BASED):
                self.__write_header(file_id, 'volScalarField', '0', 'nuTilda', '[0 2 -1 0 0 0 0]', initial_field)
            elif (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.ZERO_VELOCITY):
                self.__write_header(file_id, 'volScalarField', '0', 'nuTilda', '[0 2 -1 0 0 0 0]', 'uniform 0')
            else:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nInitial condition for nuTilda not recognised. Use either\n' +
                         'BOUNDARY_CONDITIONED_BASED or ZERO_VELOCITY and restart the solver.\n' +
                         '\n=================================== END ERROR ===================================\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__dirichlet(file_id, 'uniform ' + str(self.properties['flow_properties']['nu'] / 2))
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
                self.__empty(file_id)
            self.file_manager.write(file_id, '    }\n')

        self.file_manager.write(file_id, '}')
        self.file_manager.close_file(file_id)

    def write_nut(self):
        file_id = self.file_manager.create_file('0', 'nut')
        initial_field = 'uniform ' + str(0)
        self.__write_header(file_id, 'volScalarField', '0', 'nut', '[0 2 -1 0 0 0 0]', initial_field)
        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__nutLowReWallFunction(file_id, initial_field)
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__nutkWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
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
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
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
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
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

        if self.properties['flow_properties']['initial_conditions'] == Parameters.BOUNDARY_CONDITIONED_BASED:
            self.__write_header(file_id, 'volSymmTensorField', '0', 'R', '[0 2 -2 0 0 0 0]', initial_field)
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.ZERO_VELOCITY:
            self.__write_header(file_id, 'volSymmTensorField', '0', 'R', '[0 2 -2 0 0 0 0]', 'uniform (0 0 0 0 0 0)')
        elif self.properties['flow_properties']['initial_conditions'] == Parameters.CUSTOM:
            if (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.BOUNDARY_CONDITIONED_BASED):
                self.__write_header(file_id, 'volSymmTensorField', '0', 'R', '[0 2 -2 0 0 0 0]', initial_field)
            elif (self.properties['flow_properties']['custom_initial_conditions']
                    ['non_custom_initialised_variables_treatment'] == Parameters.ZERO_VELOCITY):
                self.__write_header(file_id, 'volSymmTensorField', '0', 'R', '[0 2 -2 0 0 0 0]',
                                    'uniform (0 0 0 0 0 0)')
            else:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nInitial condition for R (Reynolds stress tensor) not recognised. Use either\n' +
                         'BOUNDARY_CONDITIONED_BASED or ZERO_VELOCITY and restart the solver.\n' +
                         '\n=================================== END ERROR ===================================\n')

        self.file_manager.write(file_id, 'boundaryField\n{\n')
        for key in self.properties['boundary_properties']:
            self.file_manager.write(file_id, '    ' + key + '\n    {\n')
            if self.properties['boundary_properties'][key] == Parameters.WALL:
                if self.properties['turbulence_properties']['wall_modelling'] == Parameters.LOW_RE:
                    self.__dirichlet(file_id, 'uniform (0 0 0 0 0 0)')
                elif self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                    self.__kqRWallFunction(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.OUTLET:
                self.__neumann(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.BACKFLOW_OUTLET:
                self.__inlet_outlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.ADVECTIVE_OUTLET:
                self.__advective(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.SYMMETRY:
                self.__neumann(file_id)
            elif (self.properties['boundary_properties'][key] == Parameters.INLET or
                  self.properties['boundary_properties'][key] == Parameters.DFSEM_INLET):
                self.__dirichlet(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.FREESTREAM:
                self.__freestream(file_id, initial_field)
            elif self.properties['boundary_properties'][key] == Parameters.CYCLIC:
                self.__periodic(file_id)
            elif self.properties['boundary_properties'][key] == Parameters.EMPTY:
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

    def __write_dfsem_inlet(self, file_id, bc_name, initial_field):
        length_scale = self.properties['flow_properties']['reference_length']
        R = self.properties['flow_properties']['reynolds_stresses']
        L = self.properties['flow_properties']['turbulent_length_scale']
        nCellsPerEddy = self.properties['flow_properties']['number_of_cells_per_eddy']

        init_reynolds_stresses = 'uniform (' + str(R[0]) + ' ' + str(R[1]) + ' ' + str(R[2]) + ' ' + str(R[3]) + ' '\
                                 + str(R[4]) + ' ' + str(R[5]) + ')'
        init_turbulent_length_scale = 'uniform ' + str(L)

        file_id.write('        type            turbulentDFSEMInlet;\n')
        file_id.write('        delta           ' + str(length_scale) + ';\n')

        if self.properties['flow_properties']['custom_Reynolds_stresses']:
            self.file_manager.write(file_id, '        R               ')
            self.__custom_inlet_profile(file_id, bc_name, Parameters.TENSOR)
        else:
            file_id.write('        R               ' + init_reynolds_stresses + ';\n')

        if self.properties['flow_properties']['custom_velocity_inlet_profile']:
            self.file_manager.write(file_id, '        U               ')
            self.__custom_inlet_profile(file_id, bc_name, Parameters.VECTOR)
        else:
            file_id.write('        U               ' + initial_field + ';\n')

        if self.properties['flow_properties']['custom_turbulent_length_scale']:
            self.file_manager.write(file_id, '        L               ')
            self.__custom_inlet_profile(file_id, bc_name, Parameters.SCALAR)
        else:
            if self.properties['flow_properties']['set_turbulent_length_scale_at_inlet']:
                file_id.write('        L               ' + init_turbulent_length_scale + ';\n')
            else:
                file_id.write('        L               uniform 0;\n')
                file_id.write('        nCellsPerEddy   ' + str(nCellsPerEddy) + ';\n')

        file_id.write('        value           uniform (0 0 0);\n')

    def __custom_inlet_profile(self, file_id, bc_name, field_type):
        file_id.write('#codeStream\n')
        file_id.write('        {\n')
        file_id.write('            codeInclude\n')
        file_id.write('            #{\n')
        file_id.write('                #include "fvCFD.H"\n')
        file_id.write('            #};\n')
        file_id.write('\n')
        file_id.write('            codeOptions\n')
        file_id.write('            #{\n')
        file_id.write('                -I$(LIB_SRC)/finiteVolume/lnInclude \\\n')
        file_id.write('                -I$(LIB_SRC)/meshTools/lnInclude\n')
        file_id.write('            #};\n')
        file_id.write('\n')
        file_id.write('            codeLibs\n')
        file_id.write('            #{\n')
        file_id.write('                -lmeshTools \\\n')
        file_id.write('                -lfiniteVolume\n')
        file_id.write('            #};\n')
        file_id.write('\n')
        file_id.write('            code\n')
        file_id.write('            #{\n')
        file_id.write('                // get access to dictionary\n')
        file_id.write('                const IOdictionary& d = static_cast<const IOdictionary&>\n')
        file_id.write('                (\n')
        file_id.write('                    dict.parent().parent()\n')
        file_id.write('                );\n')
        file_id.write('\n')
        file_id.write('                // get access to computational mesh\n')
        file_id.write('                const fvMesh& mesh = refCast<const fvMesh>(d.db());\n')
        file_id.write('\n')
        file_id.write('                // get boundary patch ID by boundary condition name\n')
        file_id.write('                const label id = mesh.boundary().findPatchID("' + bc_name + '");\n')
        file_id.write('\n')
        file_id.write('                // get boundary patch based on ID obtained above\n')
        file_id.write('                const fvPatch& patch = mesh.boundary()[id];\n')
        file_id.write('\n')
        file_id.write('                // current (total) time\n')
        file_id.write('                const scalar currentTime = d.db().time().value();\n')
        file_id.write('\n')
        if field_type == Parameters.SCALAR:
            file_id.write('                // create new scalar field which will be written on boundary patch\n')
            file_id.write('                scalarField field = 0.0;\n')
            file_id.write('\n')
        elif field_type == Parameters.VECTOR:
            file_id.write('                // create new vector field which will be written on boundary patch\n')
            file_id.write('                vectorField field(patch.size(), vector(0, 0, 0));\n')
            file_id.write('\n')
        elif field_type == Parameters.TENSOR:
            file_id.write('                // create new tensor field which will be written on boundary patch\n')
            file_id.write('                tensorField field(patch.size(), tensor(0, 0, 0, 0, 0, 0, 0, 0, 0));\n')
            file_id.write('\n')
        file_id.write('                // loop over all boundary faces if requires\n')
        file_id.write('                forAll(field, faceI)\n')
        file_id.write('                {\n')
        file_id.write('                    // access to boundary face coordinates\n')
        file_id.write('                    const auto x = patch.Cf()[faceI].x();\n')
        file_id.write('                    const auto y = patch.Cf()[faceI].y();\n')
        file_id.write('                    const auto z = patch.Cf()[faceI].z();\n')
        file_id.write('\n')
        file_id.write('                    // set field based on location in space and time as required\n')
        file_id.write('                    if (y > 0.5)\n')
        file_id.write('                    {\n')
        if field_type == Parameters.SCALAR:
            file_id.write('                        field[faceI] = 0.01 * currentTime;\n')
        elif field_type == Parameters.VECTOR:
            file_id.write('                        field[faceI].x() =   Foam::sin(x) * Foam::cos(y) * Foam::cos(z);\n')
            file_id.write('                        field[faceI].y() = - Foam::cos(x) * Foam::sin(y) * Foam::cos(z);\n')
            file_id.write('                        field[faceI].z() =   0.0;\n')
        elif field_type == Parameters.TENSOR:
            file_id.write('                        field[faceI].xx() = 1;\n')
            file_id.write('                        field[faceI].xy() = 0;\n')
            file_id.write('                        field[faceI].xz() = 0;\n')
            file_id.write('                        field[faceI].yx() = 0;\n')
            file_id.write('                        field[faceI].yy() = 1;\n')
            file_id.write('                        field[faceI].yz() = 0;\n')
            file_id.write('                        field[faceI].zx() = 0;\n')
            file_id.write('                        field[faceI].zy() = 0;\n')
            file_id.write('                        field[faceI].zz() = 1;\n')
        file_id.write('                    }\n')
        file_id.write('                    else\n')
        file_id.write('                    {\n')
        if field_type == Parameters.SCALAR:
            file_id.write('                        field[faceI] = 0;\n')
        elif field_type == Parameters.VECTOR:
            file_id.write('                        field[faceI].x() = 0;\n')
            file_id.write('                        field[faceI].y() = 0;\n')
            file_id.write('                        field[faceI].z() = 0;\n')
        elif field_type == Parameters.TENSOR:
            file_id.write('                        field[faceI].xx() = 0;\n')
            file_id.write('                        field[faceI].xy() = 0;\n')
            file_id.write('                        field[faceI].xz() = 0;\n')
            file_id.write('                        field[faceI].yx() = 0;\n')
            file_id.write('                        field[faceI].yy() = 0;\n')
            file_id.write('                        field[faceI].yz() = 0;\n')
            file_id.write('                        field[faceI].zx() = 0;\n')
            file_id.write('                        field[faceI].zy() = 0;\n')
            file_id.write('                        field[faceI].zz() = 0;\n')
        file_id.write('                    }\n')
        file_id.write('                }\n')
        file_id.write('\n')
        file_id.write('                // set boundary values to those computed values of "field"\n')
        file_id.write('                field.writeEntry("", os);\n')
        file_id.write('            #};\n')
        file_id.write('        };\n')

    def __custom_initial_conditions(self, file_id, field_type):
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
        file_id.write('        // get the dictionary\n')
        file_id.write('        const IOdictionary& d = static_cast<const IOdictionary&>(dict);\n')
        file_id.write('\n')
        file_id.write('        // get access to the mesh\n')
        file_id.write('        const fvMesh& mesh = refCast<const fvMesh>(d.db());\n')
        file_id.write('\n')
        file_id.write('        // create a new field which will be used as the initial field\n')
        file_id.write('        vectorField field(mesh.nCells());\n')
        file_id.write('\n')
        file_id.write('        // loop over entire mesh and set values for field\n')
        file_id.write('        forAll(field, cellI)\n')
        file_id.write('        {\n')
        file_id.write('            // get access to coordinates\n')
        file_id.write('            const auto x = mesh.C()[cellI].x();\n')
        file_id.write('            const auto y = mesh.C()[cellI].y();\n')
        file_id.write('            const auto z = mesh.C()[cellI].z();\n')
        file_id.write('\n')
        file_id.write('            // set field here, overwrite for your use case here\n')
        if field_type == Parameters.SCALAR:
            file_id.write('            field[cellI] = x * y * z;\n')
        elif field_type == Parameters.VECTOR:
            file_id.write('            field[cellI].x() =   Foam::sin(x) * Foam::cos(y) * Foam::cos(z);\n')
            file_id.write('            field[cellI].y() = - Foam::cos(x) * Foam::sin(y) * Foam::cos(z);\n')
            file_id.write('            field[cellI].z() =   0.0;\n')
        elif field_type == Parameters.TENSOR:
            file_id.write('            field[cellI].xx() = 1;\n')
            file_id.write('            field[cellI].xy() = 0;\n')
            file_id.write('            field[cellI].xz() = 0;\n')
            file_id.write('            field[cellI].yx() = 0;\n')
            file_id.write('            field[cellI].yy() = 1;\n')
            file_id.write('            field[cellI].yz() = 0;\n')
            file_id.write('            field[cellI].zx() = 0;\n')
            file_id.write('            field[cellI].zy() = 0;\n')
            file_id.write('            field[cellI].zz() = 1;\n')
        file_id.write('        }\n')
        file_id.write('        field.writeEntry("", os);\n')
        file_id.write('    #};\n')
        file_id.write('};\n')
        file_id.write('\n')



