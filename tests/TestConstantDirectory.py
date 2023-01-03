import unittest
import src.CaseGenerator.WriteConstantDirectoryFiles as ConstantDir
from src.CaseGenerator.Properties import GlobalVariables as Parameters


class TestTransportPropertiesFileCreation(unittest.TestCase):
  def setUp(self):
    self.properties = {}
    self.properties['flow_properties'] = {}
    self.properties['flow_properties']['dimensional_properties'] = {}
    self.properties['flow_properties']['dimensional_properties']['nu'] = 1.2345
    self.properties['file_properties'] = {}
    self.properties['file_properties']['version'] = 'v2006'

  def test_transport_properties_file(self):
    transport_dict = ConstantDir.TransportPropertiesFile(self.properties)

    content = transport_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('transportModelNewtonian;'), -1)
    self.assertNotEqual(content.find('nu1.2345'), -1)


class TestThermophysicalPropertiesFileCreation(unittest.TestCase):
  def setUp(self):
    self.properties = {}
    self.properties['flow_properties'] = {}
    self.properties['flow_properties']['dimensional_properties'] = {}
    self.properties['flow_properties']['dimensional_properties']['mu'] = 1.2345
    self.properties['file_properties'] = {}
    self.properties['file_properties']['version'] = 'v2006'

  def test_const_viscosity(self):
    self.properties['flow_properties']['const_viscosity'] = True
    thermo_dict = ConstantDir.ThermophysicalProperties(self.properties)
    
    content = thermo_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('thermoType'), -1)
    self.assertNotEqual(content.find('typehePsiThermo;'), -1)
    self.assertNotEqual(content.find('mixturepureMixture;'), -1)
    self.assertNotEqual(content.find('transportconst;'), -1)
    self.assertNotEqual(content.find('thermohConst;'), -1)
    self.assertNotEqual(content.find('equationOfStateperfectGas;'), -1)
    self.assertNotEqual(content.find('speciespecie;'), -1)
    self.assertNotEqual(content.find('energysensibleInternalEnergy;'), -1)
    
    self.assertNotEqual(content.find('mixture'), -1)
    self.assertNotEqual(content.find('molWeight28.9;'), -1)
    self.assertNotEqual(content.find('Cp1005;'), -1)
    self.assertNotEqual(content.find('Hf0;'), -1)
    self.assertNotEqual(content.find('mu1.2345;'), -1)
    self.assertNotEqual(content.find('Pr0.71;'), -1)

  def test_variable_viscosity(self):
    self.properties['flow_properties']['const_viscosity'] = False
    thermo_dict = ConstantDir.ThermophysicalProperties(self.properties)
    
    content = thermo_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('thermoType'), -1)
    self.assertNotEqual(content.find('typehePsiThermo;'), -1)
    self.assertNotEqual(content.find('mixturepureMixture;'), -1)
    self.assertNotEqual(content.find('transportsutherland;'), -1)
    self.assertNotEqual(content.find('thermohConst;'), -1)
    self.assertNotEqual(content.find('equationOfStateperfectGas;'), -1)
    self.assertNotEqual(content.find('speciespecie;'), -1)
    self.assertNotEqual(content.find('energysensibleInternalEnergy;'), -1)
    
    self.assertNotEqual(content.find('mixture'), -1)
    self.assertNotEqual(content.find('molWeight28.9;'), -1)
    self.assertNotEqual(content.find('Cp1005;'), -1)
    self.assertNotEqual(content.find('Hf0;'), -1)
    self.assertNotEqual(content.find('As1.4792e-06;'), -1)
    self.assertNotEqual(content.find('Ts116;'), -1)

class TestTurbulencePropertiesFileCreation(unittest.TestCase):
  def setUp(self):
    self.properties = {}
    self.properties['file_properties'] = {}
    self.properties['file_properties']['version'] = 'v2006'
    self.properties['turbulence_properties'] = {}
    self.properties['turbulence_properties']['turbulence_type'] = ''

  def test_laminar(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LAMINAR
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypelaminar;'), -1)

  def test_RANS(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSST
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypeRAS;'), -1)
    self.assertNotEqual(content.find('RASModelkOmegaSST;'), -1)

  def test_SAS(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.RANS
    self.properties['turbulence_properties']['RANS_model'] = Parameters.kOmegaSSTSAS
    self.properties['turbulence_properties']['LES_model'] = Parameters.Smagorinsky
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypeRAS;'), -1)
    self.assertNotEqual(content.find('RASModelkOmegaSSTSAS;'), -1)
    self.assertNotEqual(content.find('deltacubeRootVol;'), -1)
    self.assertNotEqual(content.find('cubeRootVolCoeffs'), -1)
    self.assertNotEqual(content.find('PrandtlCoeffs'), -1)
    self.assertNotEqual(content.find('vanDriestCoeffs'), -1)
    self.assertNotEqual(content.find('smoothCoeffs'), -1)

  def test_DES(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LES
    self.properties['turbulence_properties']['LES_model'] = Parameters.SpalartAllmarasDES
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypeLES;'), -1)
    self.assertNotEqual(content.find('LESModelSpalartAllmarasDES;'), -1)
    self.assertNotEqual(content.find('deltacubeRootVol;'), -1)
    self.assertNotEqual(content.find('cubeRootVolCoeffs'), -1)
    self.assertNotEqual(content.find('PrandtlCoeffs'), -1)
    self.assertNotEqual(content.find('vanDriestCoeffs'), -1)
    self.assertNotEqual(content.find('smoothCoeffs'), -1)

  def test_DDES(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LES
    self.properties['turbulence_properties']['LES_model'] = Parameters.kOmegaSSTDDES
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypeLES;'), -1)
    self.assertNotEqual(content.find('LESModelkOmegaSSTDDES;'), -1)
    self.assertNotEqual(content.find('deltacubeRootVol;'), -1)
    self.assertNotEqual(content.find('cubeRootVolCoeffs'), -1)
    self.assertNotEqual(content.find('PrandtlCoeffs'), -1)
    self.assertNotEqual(content.find('vanDriestCoeffs'), -1)
    self.assertNotEqual(content.find('smoothCoeffs'), -1)

  def test_IDDES(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LES
    self.properties['turbulence_properties']['LES_model'] = Parameters.kOmegaSSTIDDES
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypeLES;'), -1)
    self.assertNotEqual(content.find('LESModelkOmegaSSTIDDES;'), -1)
    self.assertNotEqual(content.find('deltaIDDESDelta;'), -1)
    self.assertNotEqual(content.find('cubeRootVolCoeffs'), -1)
    self.assertNotEqual(content.find('PrandtlCoeffs'), -1)
    self.assertNotEqual(content.find('vanDriestCoeffs'), -1)
    self.assertNotEqual(content.find('smoothCoeffs'), -1)

  def test_LES(self):
    self.properties['turbulence_properties']['turbulence_type'] = Parameters.LES
    self.properties['turbulence_properties']['LES_model'] = Parameters.dynamicKEqn
    self.properties['turbulence_properties']['delta_model'] = Parameters.cubeRootVol
    self.properties['turbulence_properties']['LES_filter'] = Parameters.ANISOTROPIC_FILTER
    turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)
    
    content = turbulence_dict.get_file_content()
    content = content.replace(' ', '').replace('\t', '')

    self.assertNotEqual(content.find('simulationTypeLES;'), -1)
    self.assertNotEqual(content.find('LESModeldynamicKEqn;'), -1)
    self.assertNotEqual(content.find('deltacubeRootVol;'), -1)
    self.assertNotEqual(content.find('cubeRootVolCoeffs'), -1)
    self.assertNotEqual(content.find('PrandtlCoeffs'), -1)
    self.assertNotEqual(content.find('vanDriestCoeffs'), -1)
    self.assertNotEqual(content.find('smoothCoeffs'), -1)
    self.assertNotEqual(content.find('filteranisotropic'), -1)