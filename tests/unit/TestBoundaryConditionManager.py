import unittest
import importlib
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.Properties.GlobalVariables import *
import src.CaseGenerator.Properties.CaseProperties as CaseProperties
import src.CaseGenerator.Properties.CaseFactory as CaseFactory

class TestBoundaryConditionManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        factory = CaseFactory('Naca0012', {})
        case_handler = CaseProperties()
        cls.properties = case_handler.add_default_properties(factory.get_case_properties())

    def test_laminar_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.laminar

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'U':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typenoSlip;}', bc)
                self.assertIn('farfield{typefreestreamVelocity;freestreamValueuniform(6.00.00.0);}', bc)
                self.assertIn('BaseAndTop{typeempty;}', bc)
            if variables[index] == 'p':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typezeroGradient;}', bc)
                self.assertIn('farfield{typefreestreamPressure;freestreamValueuniform0;}', bc)
                self.assertIn('BaseAndTop{typeempty;}', bc)

    def test_epsilon_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.high_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.kEpsilon

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekqRWallFunction;', bc)
            if variables[index] == 'epsilon':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typeepsilonWallFunction;', bc)
    
    def test_epsilon_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.low_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.kEpsilon

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekLowReWallFunction;', bc)
            if variables[index] == 'epsilon':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typezeroGradient;}', bc)

    def test_omega_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.high_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSST

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekqRWallFunction;', bc)
            if variables[index] == 'omega':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typeomegaWallFunction;', bc)
    
    def test_omega_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.low_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSST

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'k':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekLowReWallFunction;', bc)
            if variables[index] == 'omega':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typeomegaWallFunction;', bc)

    def test_nut_and_nuTilda_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.high_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.SpalartAllmaras

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'nut':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typenutkWallFunction;', bc)
            if variables[index] == 'nuTilda':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typezeroGradient;', bc)
    
    def test_nut_and_nuTilda_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.low_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.SpalartAllmaras

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'nut':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typenutLowReWallFunction;', bc)
            if variables[index] == 'nuTilda':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typefixedValue;', bc)

    def test_kl_and_kt_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.high_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.kkLOmega

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'kl':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekqRWallFunction;', bc)
            if variables[index] == 'kt':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekqRWallFunction;', bc)
    
    def test_kl_and_kt_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.low_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.kkLOmega

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'kl':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typefixedValue;', bc)
            if variables[index] == 'kt':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typefixedValue;', bc)

    def test_R_high_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.high_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.LRR

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'R':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typekqRWallFunction;', bc)
    
    def test_R_low_re_boundary_conditions(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['wall_modelling'] = WallModelling.low_re
        self.properties['turbulence_properties']['RansModel'] = RansModel.LRR

        boundary_conditions = ZeroDir.BoundaryConditionManager(self.properties)
        
        [variables, bcs] = boundary_conditions.get_all_boundary_conditions()

        for index in range(0, len(variables)):
            if variables[index] == 'R':
                bc = bcs[index].replace(' ', '').replace('\t', '').replace('\n', '')
                self.assertIn('airfoil{typefixedValue;', bc)