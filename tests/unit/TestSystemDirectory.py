import unittest
import src.CaseGenerator.WriteSystemDirectoryFiles as SystemDir
from src.CaseGenerator.Properties.GlobalVariables import *
import src.CaseGenerator.Properties.CaseProperties as CaseProperties
import src.CaseGenerator.Checker as Checker


class TestTransportPropertiesFileCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cla = Checker.CheckCommandLineArguments()
        cla.add_option('case', 'Naca0012')
        case_properties_handler = CaseProperties.CaseProperties(cla)
        cls.properties = case_properties_handler.get_case_properties()

        cls.properties_decompose_par = {}
        cls.properties_decompose_par['file_properties'] = {}
        cls.properties_decompose_par['parallel_properties'] = {}
        cls.properties_decompose_par['file_properties']['version'] = 'v2006'
        cls.properties_decompose_par['parallel_properties']['run_in_parallel'] = True
        cls.properties_decompose_par['parallel_properties']['number_of_processors'] = 16

    def test_control_dict(self):
        control_dict = SystemDir.ControlDictFile(self.properties)

        content = control_dict.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('application', content)
        self.assertIn('startFrom', content)
        self.assertIn('stopAt', content)
        self.assertIn('deltaT', content)
        self.assertIn('adjustTimeStep', content)
        self.assertIn('writeControl', content)
        self.assertIn('writeInterval', content)
        self.assertIn('purgeWrite', content)
        self.assertIn('writeFormat', content)
        self.assertIn('writePrecision', content)
        self.assertIn('writeCompression', content)
        self.assertIn('timeFormat', content)
        self.assertIn('timePrecision', content)
        self.assertIn('runTimeModifiable', content)

    def test_fv_solution(self):
        fv_solution = SystemDir.fvSolutionFile(self.properties)

        content = fv_solution.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('solvers', content)
        self.assertIn('solver', content)
        self.assertIn('preconditioner', content)
        self.assertIn('UFinal', content)
        self.assertIn('pFinal', content)
        self.assertIn('nutFinal', content)
        self.assertIn('kFinal', content)
        self.assertIn('omegaFinal', content)
        self.assertIn('nCorrectors', content)
        self.assertIn('nNonOrthogonalCorrectors', content)
        self.assertIn('pRefCell', content)
        self.assertIn('pRefValue', content)
        self.assertIn('relaxationFactors', content)
        self.assertIn('fields', content)
        self.assertIn('equations', content)

    def test_fv_schemes(self):
        fv_schemes = SystemDir.fvSchemesFile(self.properties)

        content = fv_schemes.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('ddtSchemes', content)
        self.assertIn('gradSchemes', content)
        self.assertIn('grad(U)', content)
        self.assertIn('grad(p)', content)
        self.assertIn('divSchemes', content)
        self.assertIn('div(U)', content)
        self.assertIn('div(phi,U)', content)
        self.assertIn('laplacianSchemes', content)
        self.assertIn('default', content)
        self.assertIn('laplacian(p)', content)
        self.assertIn('interpolationSchemes', content)
        self.assertIn('snGradSchemes', content)
        self.assertIn('wallDist', content)
        self.assertIn('methodmeshWave', content)

    def test_decompose_par_dict(self):
        decompose_par_dict = SystemDir.WriteDecomposeParDictionary(self.properties_decompose_par)

        content = decompose_par_dict.get_decompose_par_dict()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('classdictionary;location"system";objectdecomposeParDict;', content)
        self.assertIn('numberOfSubdomains16;methodscotch;', content)