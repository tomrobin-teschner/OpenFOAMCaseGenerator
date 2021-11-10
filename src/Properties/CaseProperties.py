from src.Properties import GlobalVariables as Parameters
from math import sqrt, pow, log10, floor, sin, cos, pi
import os
import sys
import importlib
from functools import reduce


class CaseProperties:
    def __init__(self, command_line_arguments):
        properties_module = ''
        if command_line_arguments.option_exists('input'):
            properties_module = command_line_arguments['input']
        else:
            sys.exit('\n===================================== ERROR =====================================\n' +
                     '\nNo input file specify. Rerun the case generator with the --input flag\n' +
                     '\n=================================== END ERROR ===================================\n')

        try:
            file_properties = getattr(importlib.import_module('input.'+properties_module+'.'+properties_module),
                                      properties_module)
        except:
            sys.exit('Could not process the input: input/' + properties_module + '/' + properties_module + '.py\n' +
                     'Please ensure the file exists in the input directory and is spelled correctly. If it does\n' +
                     'exist, ensure that the class name within ' + properties_module + '.py contains a class of the\n'
                     'same name and derives from the base class, e.g.:\n\nclass ' + properties_module +
                     '(CPB.CasePropertiesBase):\n\nThe program will terminate now.')
        self.properties = file_properties.get_properties()

    def get_case_properties(self, command_line_arguments):
        self.__overwrite_file_properties(command_line_arguments)
        self.__add_default_properties()
        return self.properties

    def __overwrite_file_properties(self, command_line_arguments):
        if len(command_line_arguments['replace']) > 0:
            for arg in command_line_arguments['replace']:
                keys = arg.strip().split(':')[0].split('/')
                value = arg.strip().split(':')[1]
                self.__change_nested_properties(keys, value)

    def __change_nested_properties(self, keys, value):
        __doc__ = '''This is a dirty but working solution. We need to recursively update key value pairs of arbitrary
        depth but in reality we don't have more than 5 nested levels, so this solution may suffice for now. Should be
        replaced if a more recursive way can be implemented for an arbitrary depth level of the dictionary.'''
        try:
            if len(keys) == 1:
                vartype = type()
                self.properties[keys[0]] = vartype(value)
            elif len(keys) == 2:
                vartype = type(self.properties[keys[0]][keys[1]])
                self.properties[keys[0]][keys[1]] = vartype(value)
            elif len(keys) == 3:
                vartype = type(self.properties[keys[0]][keys[1]][keys[2]])
                self.properties[keys[0]][keys[1]][keys[2]] = vartype(value)
            elif len(keys) == 4:
                vartype = type(self.properties[keys[0]][keys[1]][keys[2]][keys[3]])
                self.properties[keys[0]][keys[1]][keys[2]][keys[3]] = vartype(value)
            elif len(keys) == 5:
                vartype = type(self.properties[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]])
                self.properties[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]] = vartype(value)
            elif len(keys) == 6:
                vartype = type(self.properties[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]])
                self.properties[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]] = vartype(value)
            elif len(keys) == 7:
                vartype = type(self.properties[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][keys[6]])
                self.properties[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]][keys[6]] = vartype(value)
        except:
            sys.exit('Trying to replace the entry ' + str(keys) + ' which does not exist in the properties dictionary.'
                     '\nEnsure that it is correctly spelled and try again')

        # only append parameters to case name if it does not contain forward / backward slashes which may be seen as
        # directory separators
        if (value.find('\\') == -1) and (value.find('/') == -1):
            self.__append_replaced_parameters_to_case_name(keys[-1], value)

    def __append_replaced_parameters_to_case_name(self, key, value):
        print(self.properties['file_properties']['case_name'])
        self.properties['file_properties']['case_name'] += '_' + str(key) + '_' + str(value)
        print(self.properties['file_properties']['case_name'])

    def __add_default_properties(self):
        # absolute path of text case location
        self.properties['file_properties']['path'] = os.path.join(self.properties['file_properties']['run_directory'],
                                                                  self.properties['file_properties']['case_name'])

        # check how quantities are specified and calculate the missing properties
        if self.properties['flow_properties']['input_parameters_specification_mode'] == Parameters.NON_DIMENSIONAL:
            if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
                self.__calculate_dimensional_properties_from_Re_incompressible()
            elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
                self.__calculate_dimensional_properties_from_Ma_compressible()
        if self.properties['flow_properties']['input_parameters_specification_mode'] == Parameters.DIMENSIONAL:
            self.__calculate_Re_incompressible_from_dimensional_properties()
            if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
                self.__calculate_Ma_compressible_from_dimensional_properties()

        self.__add_dynamic_viscosity()
        self.__create_inlet_velocity_vector_from_velocity_magnitude_and_direction()
        self.__set_correct_gradient_reconstruction_scheme_for_RANS()

    def __calculate_dimensional_properties_from_Re_incompressible(self):
        Re = self.properties['flow_properties']['non_dimensional_properties']['Re']
        l_ref = self.properties['dimensionless_coefficients']['reference_length']
        order_of_magnitude = floor(log10(Re))
        nu = 1.0 / pow(10, order_of_magnitude)
        u_mag = Re * nu / l_ref

        self.properties['flow_properties']['dimensional_properties']['nu'] = nu
        self.properties['flow_properties']['dimensional_properties']['rho'] = 1.0
        self.properties['flow_properties']['dimensional_properties']['p'] = 0
        self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = u_mag

    def __calculate_dimensional_properties_from_Ma_compressible(self):
        T = 298
        Ma = self.properties['flow_properties']['non_dimensional_properties']['Ma']
        c = sqrt(1.4 * 287 * T)
        self.properties['flow_properties']['dimensional_properties']['speed_of_sound'] = c
        u_mag = Ma * c
        Re = self.properties['flow_properties']['non_dimensional_properties']['Re']
        l_ref = self.properties['dimensionless_coefficients']['reference_length']
        nu = u_mag * l_ref / Re

        self.properties['flow_properties']['dimensional_properties']['nu'] = nu
        self.properties['flow_properties']['dimensional_properties']['rho'] = 1.225
        self.properties['flow_properties']['dimensional_properties']['T'] = T
        self.properties['flow_properties']['dimensional_properties']['p'] = 1e5
        self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = u_mag

    def __calculate_Re_incompressible_from_dimensional_properties(self):
        # calculate reynolds number
        u_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        l_ref = self.properties['dimensionless_coefficients']['reference_length']
        self.properties['flow_properties']['non_dimensional_properties']['Re'] = u_mag * l_ref / nu

    def __calculate_Ma_compressible_from_dimensional_properties(self):
        u_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        T = self.properties['flow_properties']['dimensional_properties']['T']
        c = sqrt(1.4 * 287 * T)
        self.properties['flow_properties']['non_dimensional_properties']['speed_of_sound'] = c
        self.properties['flow_properties']['non_dimensional_properties']['Ma'] = u_mag / c

    def __add_dynamic_viscosity(self):
        nu = self.properties['flow_properties']['dimensional_properties']['nu']
        rho = self.properties['flow_properties']['dimensional_properties']['rho']
        self.properties['flow_properties']['dimensional_properties']['mu'] = nu * rho

    def __create_inlet_velocity_vector_from_velocity_magnitude_and_direction(self):
        velocity_vector = [0.0, 0.0, 0.0]
        RAD_TO_DEG = pi / 180

        tangential = self.properties['flow_properties']['axis_aligned_flow_direction']['tangential']
        normal = self.properties['flow_properties']['axis_aligned_flow_direction']['normal']
        aoa = self.properties['flow_properties']['axis_aligned_flow_direction']['angle_of_attack']
        u_mag = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']

        velocity_vector[tangential] = cos(aoa * RAD_TO_DEG) * u_mag
        velocity_vector[normal] = sin(aoa * RAD_TO_DEG) * u_mag

        self.properties['flow_properties']['dimensional_properties']['velocity_vector'] = velocity_vector

    def __set_correct_gradient_reconstruction_scheme_for_RANS(self):
        self.properties['turbulence_properties']['use_phi_instead_of_grad_U'] = False,
        if (self.properties['turbulence_properties']['RANS_model'] == Parameters.LienCubicKE or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.ShihQuadraticKE or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.LRR or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.SSG):
            self.properties['turbulence_properties']['use_phi_instead_of_grad_U'] = True
