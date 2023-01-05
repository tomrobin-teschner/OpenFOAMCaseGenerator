import unittest
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.Properties import GlobalVariables as Parameters


class TestBoundaryConditionManager(unittest.TestCase):
    def setUp(self):
        self.properties = {}

        self.properties['file_properties'] = {}
        self.properties['flow_properties'] = {}
        self.properties['turbulence_properties'] = {}
        self.properties['dimensionless_coefficients'] = {}

        self.properties['file_properties']['version'] = 'v2006'

        self.properties['flow_properties']['dimensional_properties'] = {}
        self.properties['flow_properties']['non_dimensional_properties'] = {}
        self.properties['flow_properties']['flow_type'] = Parameters.incompressible
        self.properties['flow_properties']['initial_conditions'] = Parameters.BOUNDARY_CONDITIONED_BASED
        self.properties['flow_properties']['custom_initial_conditions'] = False
        self.properties['flow_properties']['custom_initial_conditions_setup'] = ''

        self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = 1.0
        self.properties['flow_properties']['dimensional_properties']['velocity_vector'] = [1.0, 0.0, 0.0]
        self.properties['flow_properties']['dimensional_properties']['T'] = 5.0
        self.properties['flow_properties']['dimensional_properties']['nu'] = 1e-6
        self.properties['flow_properties']['non_dimensional_properties']['Re'] = 6000000
        self.properties['dimensionless_coefficients']['reference_length'] = 1.0

        self.properties['turbulence_properties']['freestream_turbulent_intensity'] = 0.01
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.LOW_RE
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = Parameters.EXTERNAL
        self.properties['turbulence_properties']['turbulent_to_laminar_ratio'] = 10.0
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSST

        self.properties['boundary_properties'] = {}
        self.properties['boundary_properties']['boundary_conditions'] = {}
        self.properties['boundary_properties']['boundary_conditions']['inlet'] = Parameters.INLET
        self.properties['boundary_properties']['boundary_conditions']['freestream'] = Parameters.FREESTREAM
        self.properties['boundary_properties']['boundary_conditions']['outlet'] = Parameters.OUTLET
        self.properties['boundary_properties']['boundary_conditions']['inletoutlet'] = Parameters.INLET_OUTLET
        self.properties['boundary_properties']['boundary_conditions']['advective'] = Parameters.ADVECTIVE_OUTLET
        self.properties['boundary_properties']['boundary_conditions']['wall'] = Parameters.WALL
        self.properties['boundary_properties']['boundary_conditions']['symmetry'] = Parameters.SYMMETRY
        self.properties['boundary_properties']['boundary_conditions']['cyclic'] = Parameters.CYCLIC
        self.properties['boundary_properties']['boundary_conditions']['empty'] = Parameters.EMPTY

        self.properties['boundary_properties']['custom_inlet_boundary_conditions'] = False
        self.properties['boundary_properties']['custom_inlet_boundary_conditions_setup'] = ''


    def test_laminar_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.LAMINAR

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'U':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('inlet{typefixedValue;valueuniform(1.00.00.0);}', bc)
                self.assertIn('freestream{typefreestreamVelocity;freestreamValueuniform(1.00.00.0);}', bc)
                self.assertIn('outlet{typezeroGradient;}', bc)
                self.assertIn('inletoutlet{typefreestreamVelocity;freestreamValueuniform(1.00.00.0);}', bc)
                self.assertIn('advective{typeadvective;phiphi;}', bc)
                self.assertIn('wall{typenoSlip;}', bc)
                self.assertIn('symmetry{typezeroGradient;}', bc)
                self.assertIn('cyclic{typecyclic;}', bc)
                self.assertIn('empty{typeempty;}', bc)
            if variables[index] is 'p':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('inlet{typezeroGradient;}', bc)
                self.assertIn('freestream{typefreestreamPressure;freestreamValueuniform0;}', bc)
                self.assertIn('outlet{typefixedValue;valueuniform0;}', bc)
                self.assertIn('inletoutlet{typefreestreamPressure;freestreamValueuniform0;}', bc)
                self.assertIn('advective{typeadvective;phiphi;}', bc)
                self.assertIn('wall{typezeroGradient;}', bc)
                self.assertIn('symmetry{typezeroGradient;}', bc)
                self.assertIn('cyclic{typecyclic;}', bc)
                self.assertIn('empty{typeempty;}', bc)

    def test_epsilon_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.HIGH_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kEpsilon

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekqRWallFunction;', bc)
            if variables[index] is 'epsilon':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typeepsilonWallFunction;', bc)
    
    def test_epsilon_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.LOW_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kEpsilon

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekLowReWallFunction;', bc)
            if variables[index] is 'epsilon':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typezeroGradient;}', bc)

    def test_omega_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.HIGH_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSST

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekqRWallFunction;', bc)
            if variables[index] is 'omega':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typeomegaWallFunction;', bc)
    
    def test_omega_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.LOW_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSST

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekLowReWallFunction;', bc)
            if variables[index] is 'omega':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typeomegaWallFunction;', bc)

    def test_nut_and_nuTilda_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.HIGH_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.SpalartAllmaras

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'nut':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typenutkWallFunction;', bc)
            if variables[index] is 'nuTilda':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typezeroGradient;', bc)
    
    def test_nut_and_nuTilda_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.LOW_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.SpalartAllmaras

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'nut':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typenutLowReWallFunction;', bc)
            if variables[index] is 'nuTilda':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typefixedValue;', bc)

    def test_kl_and_kt_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.HIGH_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kkLOmega

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'kl':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekqRWallFunction;', bc)
            if variables[index] is 'kt':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekqRWallFunction;', bc)
    
    def test_kl_and_kt_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.LOW_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.kkLOmega

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'kl':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typefixedValue;', bc)
            if variables[index] is 'kt':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typefixedValue;', bc)

    def test_R_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.HIGH_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.LRR

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'R':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typekqRWallFunction;', bc)
    
    def test_R_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
        self.properties['turbulence_properties']['wall_modelling'] = Parameters.LOW_RE
        self.properties['turbulence_properties']['RANS_model'] = Parameters.LRR

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] is 'R':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('wall{typefixedValue;', bc)