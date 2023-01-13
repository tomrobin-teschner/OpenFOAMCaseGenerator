import unittest
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.Properties.GlobalVariables import *

class TestStateVariableManager(unittest.TestCase):
    def setUp(self):
        self.properties = {}
        self.properties['file_properties'] = {}
        self.properties['file_properties']['version'] = 'v2006'
        self.properties['flow_properties'] = {}
        self.properties['flow_properties']['flow_type'] = FlowType.incompressible 
        self.properties['turbulence_properties'] = {}
        self.properties['turbulence_properties']['turbulence_type'] = ''

    def test_laminar_incompressible(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.laminar
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)
        
        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertNotIn('T', state_variables_names)

    def test_laminar_compressible(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.laminar
        self.properties['flow_properties']['flow_type'] = FlowType.compressible 
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)
        
        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('T', state_variables_names)

    def test_RANS_kEpsilon(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kEpsilon
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_realizableKE(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.realizableKE
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_RNGkEpsilon(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.RNGkEpsilon
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_LienLeschziner(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.LienLeschziner
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_LamBremhorstKE(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.LamBremhorstKE
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_LaunderSharmaKE(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.LaunderSharmaKE
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_kOmega(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmega
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('omega', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_kOmegaSST(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSST
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('omega', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_qZeta(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.qZeta
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_SpalartAllmaras(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.SpalartAllmaras
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('nuTilda', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_kOmegaSSTLM(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSSTLM
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('omega', state_variables_names)
        self.assertIn('nut', state_variables_names)
        self.assertIn('gammaInt', state_variables_names)
        self.assertIn('ReThetat', state_variables_names)

    def test_RANS_kkLOmega(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kkLOmega
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('kl', state_variables_names)
        self.assertIn('kt', state_variables_names)
        self.assertIn('omega', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_kOmegaSSTSAS(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSSTSAS
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('omega', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_LienCubicKE(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.LienCubicKE
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_ShihQuadraticKE(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.ShihQuadraticKE
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_LRR(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.LRR
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('R', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_RANS_SSG(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.SSG
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('R', state_variables_names)
        self.assertIn('epsilon', state_variables_names)
        self.assertIn('nut', state_variables_names)

    def test_DES(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.les
        self.properties['turbulence_properties']['LesModel'] = LesModel.SpalartAllmarasDES
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
        self.properties['turbulence_properties']['LesFilter'] = LesFilter.anisotropic
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('nut', state_variables_names)
        self.assertIn('nuTilda', state_variables_names)

    def test_LES(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.les
        self.properties['turbulence_properties']['LesModel'] = LesModel.dynamicKEqn
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
        self.properties['turbulence_properties']['LesFilter'] = LesFilter.anisotropic
        state_variable_manager = ZeroDir.StateVariableManager(self.properties)

        state_variables_names = state_variable_manager.get_active_variable_names()

        self.assertIn('U', state_variables_names)
        self.assertIn('p', state_variables_names)
        self.assertIn('k', state_variables_names)
        self.assertIn('nut', state_variables_names)
