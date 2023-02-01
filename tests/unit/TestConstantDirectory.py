import unittest
import src.CaseGenerator.WriteConstantDirectoryFiles as ConstantDir
from src.CaseGenerator.Properties.GlobalVariables import *
import src.CaseGenerator.Properties.CaseProperties as CaseProperties
import src.CaseGenerator.Properties.CaseFactory as CaseFactory


class TestTransportPropertiesFileCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        factory = CaseFactory.CaseFactory('Naca0012', {})
        case_handler = CaseProperties.CaseProperties()
        cls.properties = case_handler.add_default_properties(factory.get_case_properties())

    def test_transport_properties_file(self):
        transport_dict = ConstantDir.TransportPropertiesFile(self.properties)

        content = transport_dict.get_file_content()
        content = content.replace(' ', '').replace('\t', '')

        self.assertNotEqual(content.find('transportModelNewtonian;'), -1)
        self.assertNotEqual(content.find('nu1e-06'), -1)


class TestThermophysicalPropertiesFileCreation(unittest.TestCase):
    def setUp(self):
        self.properties = {}
        self.properties['flow_properties'] = {}
        self.properties['flow_properties']['equation_of_state'] = EquationOfState.perfectGas
        self.properties['flow_properties']['energy_equation'] = EnergyEquation.sensibleInternalEnergy
        self.properties['flow_properties']['dimensional_properties'] = {}
        self.properties['flow_properties']['dimensional_properties']['material_properties'] = {}
        self.properties['flow_properties']['dimensional_properties']['material_properties']['mu'] = 1.2345
        self.properties['flow_properties']['dimensional_properties']['material_properties']['Pr'] = 0.71
        self.properties['flow_properties']['dimensional_properties']['material_properties']['Hf'] = 0
        self.properties['flow_properties']['dimensional_properties']['material_properties']['Cp'] = 1005
        self.properties['flow_properties']['dimensional_properties']['material_properties']['molWeight'] = 28.9
        self.properties['flow_properties']['dimensional_properties']['material_properties']['As'] = 1.4792e-06
        self.properties['flow_properties']['dimensional_properties']['material_properties']['Ts'] = 116
        self.properties['file_properties'] = {}
        self.properties['file_properties']['version'] = 'v2212'

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
        self.properties['file_properties']['version'] = 'v2212'
        self.properties['turbulence_properties'] = {}
        self.properties['turbulence_properties']['turbulence_type'] = ''

    def test_laminar(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.laminar
        turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)

        content = turbulence_dict.get_file_content()
        content = content.replace(' ', '').replace('\t', '')

        self.assertNotEqual(content.find('simulationTypelaminar;'), -1)

    def test_RANS(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSST
        turbulence_dict = ConstantDir.TurbulencePropertiesFile(self.properties)

        content = turbulence_dict.get_file_content()
        content = content.replace(' ', '').replace('\t', '')

        self.assertNotEqual(content.find('simulationTypeRAS;'), -1)
        self.assertNotEqual(content.find('RASModelkOmegaSST;'), -1)

    def test_SAS(self):
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.rans
        self.properties['turbulence_properties']['RansModel'] = RansModel.kOmegaSSTSAS
        self.properties['turbulence_properties']['LesModel'] = LesModel.Smagorinsky
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
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
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.les
        self.properties['turbulence_properties']['LesModel'] = LesModel.SpalartAllmarasDES
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
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
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.les
        self.properties['turbulence_properties']['LesModel'] = LesModel.kOmegaSSTDDES
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
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
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.les
        self.properties['turbulence_properties']['LesModel'] = LesModel.kOmegaSSTIDDES
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
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
        self.properties['turbulence_properties']['turbulence_type'] = TurbulenceType.les
        self.properties['turbulence_properties']['LesModel'] = LesModel.dynamicKEqn
        self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.cubeRootVol
        self.properties['turbulence_properties']['LesFilter'] = LesFilter.anisotropic
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
