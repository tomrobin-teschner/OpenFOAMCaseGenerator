from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator.Properties.CaseFactory import CaseFactory
from math import sqrt, pow, log10, floor, sin, cos, pi
import os


class CaseProperties:
    def __init__(self, command_line_arguments):
        factory = CaseFactory(command_line_arguments['case'], command_line_arguments['parameter'])
        self.properties = factory.get_case_properties()

    def get_case(self):
        self.__add_default_properties()
        return self.properties

    def __add_default_properties(self):
        # absolute path of text case location
        self.properties['file_properties']['path'] = os.path.join(self.properties['file_properties']['run_directory'],
                                                                  self.properties['file_properties']['case_name'])

        # check how quantities are specified and calculate the missing properties
        if self.properties['flow_properties']['input_parameters_specification_mode'] == Dimensionality.non_dimensional:
            if self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
                self.__calculate_dimensional_properties_from_Re_incompressible()
            elif self.properties['flow_properties']['flow_type'] == FlowType.compressible:
                self.__calculate_dimensional_properties_from_Ma_compressible()
        if self.properties['flow_properties']['input_parameters_specification_mode'] == Dimensionality.dimensional:
            self.__calculate_Re_incompressible_from_dimensional_properties()
            if self.properties['flow_properties']['flow_type'] == FlowType.compressible:
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

        velocity_vector[tangential.value] = cos(aoa * RAD_TO_DEG) * u_mag
        velocity_vector[normal.value] = sin(aoa * RAD_TO_DEG) * u_mag

        self.properties['flow_properties']['dimensional_properties']['velocity_vector'] = velocity_vector

    def __set_correct_gradient_reconstruction_scheme_for_RANS(self):
        self.properties['turbulence_properties']['use_phi_instead_of_grad_U'] = False
        RansModel = self.properties['turbulence_properties']['RansModel']
        if (RansModel == RansModel.LienCubicKE or
                RansModel == RansModel.ShihQuadraticKE or
                RansModel == RansModel.LRR or
                RansModel == RansModel.SSG):
            self.properties['turbulence_properties']['use_phi_instead_of_grad_U'] = True
