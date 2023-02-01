from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator.Properties.CaseFactory import CaseFactory
from math import sqrt, pow, log10, floor, sin, cos, pi
import importlib
import os


class CaseProperties:
    def __init__(self):
        self.material = object()

    def add_default_properties(self, properties):
        # absolute path of text case location
        properties['file_properties']['path'] = os.path.join(properties['file_properties']['run_directory'],
                                                                  properties['file_properties']['case_name'])
        # set default properties, overwrite below if required
        properties = self.__get_material_properties(properties)

        # check how quantities are specified and calculate the missing properties
        if properties['flow_properties']['input_parameters_specification_mode'] == Dimensionality.non_dimensional:
            if properties['flow_properties']['flow_type'] == FlowType.incompressible:
                properties = self.__calculate_dimensional_properties_from_Re_incompressible(properties)
            elif properties['flow_properties']['flow_type'] == FlowType.compressible:
                properties = self.__calculate_dimensional_properties_from_Ma_compressible(properties)
        if properties['flow_properties']['input_parameters_specification_mode'] == Dimensionality.dimensional:
            properties = self.__calculate_Re_incompressible_from_dimensional_properties(properties)
            if properties['flow_properties']['flow_type'] == FlowType.compressible:
                properties = self.__calculate_Ma_compressible_from_dimensional_properties(properties)

        properties = self.__create_inlet_velocity_vector_from_velocity_magnitude_and_direction(properties)
        properties = self.__set_correct_gradient_reconstruction_scheme_for_RANS(properties)
        return properties

    def __get_material_properties(self, properties):
        name = properties['flow_properties']['dimensional_properties']['material'].name
        material_module = getattr(importlib.import_module(f'input.fluids.{name}'), name)
        
        material_properties = properties['flow_properties']['dimensional_properties']['material_properties']

        self.material = material_module(**material_properties)
        properties['flow_properties']['dimensional_properties']['material_properties']['rho'] = self.material.get('rho')
        properties['flow_properties']['dimensional_properties']['material_properties']['p'] = self.material.get('p')
        properties['flow_properties']['dimensional_properties']['material_properties']['T'] = self.material.get('T')
        properties['flow_properties']['dimensional_properties']['material_properties']['Ts'] = self.material.get('Ts')
        properties['flow_properties']['dimensional_properties']['material_properties']['mu'] = self.material.get('mu')
        properties['flow_properties']['dimensional_properties']['material_properties']['nu'] = self.material.get('nu')
        properties['flow_properties']['dimensional_properties']['material_properties']['R'] = self.material.get('R')
        properties['flow_properties']['dimensional_properties']['material_properties']['gamma'] = self.material.get('gamma')
        properties['flow_properties']['dimensional_properties']['material_properties']['Pr'] = self.material.get('Pr')
        properties['flow_properties']['dimensional_properties']['material_properties']['As'] = self.material.get('As')
        properties['flow_properties']['dimensional_properties']['material_properties']['molWeight'] = self.material.get('molWeight')
        properties['flow_properties']['dimensional_properties']['material_properties']['Cp'] = self.material.get('Cp')
        properties['flow_properties']['dimensional_properties']['material_properties']['Hf'] = self.material.get('Hf')
        
        return properties

    def __calculate_dimensional_properties_from_Re_incompressible(self, properties):
        Re = properties['flow_properties']['non_dimensional_properties']['Re']
        l_ref = properties['dimensionless_coefficients']['reference_length']
        order_of_magnitude = floor(log10(Re))
        nu = 1.0 / pow(10, order_of_magnitude)
        u_mag = Re * nu / l_ref

        if properties['flow_properties']['equations'] == Equations.euler:
            properties['flow_properties']['dimensional_properties']['material_properties']['nu'] = 0.0
            properties['flow_properties']['dimensional_properties']['material_properties']['mu'] = 0.0
        else:
            properties['flow_properties']['dimensional_properties']['material_properties']['nu'] = nu

        properties['flow_properties']['dimensional_properties']['material_properties']['rho'] = 1.0
        properties['flow_properties']['dimensional_properties']['material_properties']['p'] = 0
        properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = u_mag
        return properties

    def __calculate_dimensional_properties_from_Ma_compressible(self, properties):
        T = self.material.get('T')
        R = self.material.get('R')
        gamma = self.material.get('gamma')
        Ma = properties['flow_properties']['non_dimensional_properties']['Ma']
        
        c = sqrt(gamma * R * T)
        properties['flow_properties']['dimensional_properties']['material_properties']['speed_of_sound'] = c
        u_mag = Ma * c
        Re = properties['flow_properties']['non_dimensional_properties']['Re']
        l_ref = properties['dimensionless_coefficients']['reference_length']
        nu = u_mag * l_ref / Re

        if properties['flow_properties']['equations'] == Equations.euler:
            properties['flow_properties']['dimensional_properties']['material_properties']['nu'] = 0.0
            properties['flow_properties']['dimensional_properties']['material_properties']['mu'] = 0.0
        else:
            properties['flow_properties']['dimensional_properties']['material_properties']['nu'] = nu

        properties['flow_properties']['dimensional_properties']['material_properties']['rho'] = self.material.get('rho')
        properties['flow_properties']['dimensional_properties']['material_properties']['T'] = self.material.get('T')
        properties['flow_properties']['dimensional_properties']['material_properties']['p'] = self.material.get('p')
        properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = u_mag
        return properties

    def __calculate_Re_incompressible_from_dimensional_properties(self, properties):
        # calculate reynolds number
        u_mag = properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        nu = properties['flow_properties']['dimensional_properties']['material_properties']['nu']
        l_ref = properties['dimensionless_coefficients']['reference_length']
        properties['flow_properties']['non_dimensional_properties']['Re'] = u_mag * l_ref / nu
        return properties

    def __calculate_Ma_compressible_from_dimensional_properties(self, properties):
        T = self.material.get('T')
        R = self.material.get('R')
        gamma = self.material.get('gamma')
        u_mag = properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        c = sqrt(gamma * R * T)
        properties['flow_properties']['dimensional_properties']['material_properties']['speed_of_sound'] = c
        properties['flow_properties']['non_dimensional_properties']['Ma'] = u_mag / c
        return properties

    def __create_inlet_velocity_vector_from_velocity_magnitude_and_direction(self, properties):
        velocity_vector = [0.0, 0.0, 0.0]
        RAD_TO_DEG = pi / 180

        tangential = properties['flow_properties']['axis_aligned_flow_direction']['tangential']
        normal = properties['flow_properties']['axis_aligned_flow_direction']['normal']
        aoa = properties['flow_properties']['axis_aligned_flow_direction']['angle_of_attack']
        u_mag = properties['flow_properties']['dimensional_properties']['velocity_magnitude']

        velocity_vector[tangential.value] = cos(aoa * RAD_TO_DEG) * u_mag
        velocity_vector[normal.value] = sin(aoa * RAD_TO_DEG) * u_mag

        properties['flow_properties']['dimensional_properties']['velocity_vector'] = velocity_vector
        return properties

    def __set_correct_gradient_reconstruction_scheme_for_RANS(self, properties):
        properties['turbulence_properties']['use_phi_instead_of_grad_U'] = False
        RansModel = properties['turbulence_properties']['RansModel']
        if (RansModel == RansModel.LienCubicKE or
                RansModel == RansModel.ShihQuadraticKE or
                RansModel == RansModel.LRR or
                RansModel == RansModel.SSG):
            properties['turbulence_properties']['use_phi_instead_of_grad_U'] = True
        return properties
