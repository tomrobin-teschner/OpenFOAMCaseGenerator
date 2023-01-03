import unittest
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.Properties import GlobalVariables as Parameters


class TestStateVariableManager(unittest.TestCase):
  def setUp(self):
    self.properties = {}
    self.properties['file_properties'] = {}
    self.properties['file_properties']['version'] = 'v2006'
    self.properties['flow_properties'] = {}
    self.properties['flow_properties']['flow_type'] = Parameters.incompressible 
    self.properties['turbulence_properties'] = {}
    self.properties['turbulence_properties']['turbulence_type'] = ''

  def test_laminar_incompressible(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LAMINAR
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertNotIn('T', state_variables)

  def test_laminar_compressible(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LAMINAR
    self.properties['flow_properties']['flow_type'] = Parameters.compressible 
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('T', state_variables)

  def test_RANS_kEpsilon(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kEpsilon
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_realizableKE(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.realizableKE
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_RNGkEpsilon(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.RNGkEpsilon
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_LienLeschziner(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.LienLeschziner
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_LamBremhorstKE(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.LamBremhorstKE
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_LaunderSharmaKE(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.LaunderSharmaKE
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_kOmega(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmega
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('omega', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_kOmegaSST(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSST
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('omega', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_qZeta(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.qZeta
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_SpalartAllmaras(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.SpalartAllmaras
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('nuTilda', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_kOmegaSSTLM(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSSTLM
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('omega', state_variables)
    self.assertIn('nut', state_variables)
    self.assertIn('gammaInt', state_variables)
    self.assertIn('ReThetat', state_variables)

  def test_RANS_kkLOmega(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kkLOmega
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('kl', state_variables)
    self.assertIn('kt', state_variables)
    self.assertIn('omega', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_kOmegaSSTSAS(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSSTSAS
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('omega', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_LienCubicKE(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.LienCubicKE
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_ShihQuadraticKE(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.ShihQuadraticKE
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_LRR(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.LRR
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('R', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_RANS_SSG(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.SSG
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('R', state_variables)
    self.assertIn('epsilon', state_variables)
    self.assertIn('nut', state_variables)

  def test_DES(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LES
    self.properties['turbulence_properties']['LES_model'] = Parameters.SpalartAllmarasDES
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    self.properties['turbulence_properties']['LES_filter'] = Parameters.ANISOTROPIC_FILTER
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('nut', state_variables)
    self.assertIn('nuTilda', state_variables)

  def test_LES(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LES
    self.properties['turbulence_properties']['LES_model'] = Parameters.dynamicKEqn
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    self.properties['turbulence_properties']['LES_filter'] = Parameters.ANISOTROPIC_FILTER
    state_variable_manager = ZeroDir.StateVariableManager(self.properties)
    
    state_variables = state_variable_manager.get_active_variables()

    self.assertIn('U', state_variables)
    self.assertIn('p', state_variables)
    self.assertIn('k', state_variables)
    self.assertIn('nut', state_variables)
