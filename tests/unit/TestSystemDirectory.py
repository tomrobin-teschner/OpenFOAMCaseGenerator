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

        cls.properties['point_probes']['write_point_probes'] = True
        cls.properties['point_probes']['location'] = [[0.0, 0.0, 0.0]]
        cls.properties['point_probes']['variables_to_monitor'] = ['U']
        
        cls.properties['line_probes']['write_line_probes'] = True
        cls.properties['line_probes']['location'] = {
            'name': 'x-axis',
            'start': [0.0, 0.0, 0.0],
            'end': [1.0, 0.0, 0.0],
        },
        cls.properties['line_probes']['variables_to_monitor'] = ['U']
        
        cls.properties['cutting_planes']['write_cutting_planes'] = True
        cls.properties['cutting_planes']['location'] = {
            'name': 'plane_x=0',
            'origin': [0, 0, 0],
            'normal': [1, 0, 0],
        },
        cls.properties['cutting_planes']['variables_to_monitor'] = ['U']

        cls.properties['iso_surfaces']['write_iso_surfaces'] = True
        cls.properties['iso_surfaces']['flow_variable'] = ['U']
        cls.properties['iso_surfaces']['iso_value'] = [0.1]

        cls.properties_decompose_par = {}
        cls.properties_decompose_par['file_properties'] = {}
        cls.properties_decompose_par['parallel_properties'] = {}
        cls.properties_decompose_par['file_properties']['version'] = 'v2212'
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
        decompose_par_dict = SystemDir.DecomposeParDictionary(self.properties_decompose_par)

        content = decompose_par_dict.get_decompose_par_dict()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('classdictionary;location"system";objectdecomposeParDict;', content)
        self.assertIn('numberOfSubdomains16;methodscotch;', content)

    def test_force_coefficients(self):
        force_coefficients = SystemDir.ForceCoefficients(self.properties)

        content = force_coefficients.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('forceCoefficiens', content)
        self.assertIn('typeforceCoeffs;', content)
        self.assertIn('libs(forces);', content)
        self.assertIn('writeControl', content)
        self.assertIn('timeInterval', content)
        self.assertIn('log', content)
        self.assertIn('patches', content)
        self.assertIn('rho', content)
        self.assertIn('liftDir', content)
        self.assertIn('dragDir', content)
        self.assertIn('CofR', content)
        self.assertIn('pitchAxis', content)
        self.assertIn('magUInf', content)
        self.assertIn('lRef', content)
        self.assertIn('Aref', content)

    def test_force_coefficient_triggers(self):
        triggers = SystemDir.ForceCoefficientConvergence(self.properties)

        content = triggers.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('forceCoefficientConvergenceTrigger', content)
        self.assertIn('typerunTimeControl;', content)
        self.assertIn('libs(utilityFunctionObjects);', content)
        self.assertIn('conditions', content)

    def test_cp_coefficient(self):
        cp = SystemDir.PressureCoefficient(self.properties)

        content = cp.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('pressureCoefficient', content)
        self.assertIn('typepressure;', content)
        self.assertIn('libs(fieldFunctionObjects);', content)
        self.assertIn('writeControl', content)
        self.assertIn('mode', content)
        self.assertIn('result', content)
        self.assertIn('rho', content)
        self.assertIn('pInf', content)
        self.assertIn('UInf', content)

    def test_point_probes(self):
        points = SystemDir.PointProbes(self.properties)

        content = points.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('sampling', content)
        self.assertIn('typeprobes;', content)
        self.assertIn('libs(fieldFunctionObjects);', content)
        self.assertIn('writeControl', content)
        self.assertIn('writeInterval', content)
        self.assertIn('log', content)
        self.assertIn('probeLocations', content)
        self.assertIn('fields', content)

    def test_line_probes(self):
        lines = SystemDir.LineProbes(self.properties)

        content = lines.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('sampling', content)
        self.assertIn('typesets;', content)
        self.assertIn('libs(sampling);', content)
        self.assertIn('interpolationScheme', content)
        self.assertIn('setFormat', content)
        self.assertIn('writeControl', content)
        self.assertIn('log', content)
        self.assertIn('sets', content)
        self.assertIn('axis', content)
        self.assertIn('start', content)
        self.assertIn('end', content)
        self.assertIn('sets', content)
        self.assertIn('nPoints', content)

    def test_cutting_planes(self):
        planes = SystemDir.CuttingPlanes(self.properties)

        content = planes.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('sampling', content)
        self.assertIn('typesurfaces;', content)
        self.assertIn('libs(sampling);', content)
        self.assertIn('interpolationScheme', content)
        self.assertIn('surfaceFormat', content)
        self.assertIn('writeControl', content)
        self.assertIn('log', content)
        self.assertIn('surfaces', content)
        self.assertIn('planeType', content)
        self.assertIn('interpolate', content)
        self.assertIn('fields', content)

    def test_iso_surfaces(self):
        iso = SystemDir.IsoSurfaces(self.properties)

        content = iso.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('sampling', content)
        self.assertIn('typesurfaces;', content)
        self.assertIn('libs(sampling);', content)
        self.assertIn('interpolationScheme', content)
        self.assertIn('surfaceFormat', content)
        self.assertIn('writeControl', content)
        self.assertIn('log', content)
        self.assertIn('surfaces', content)
        self.assertIn('isoField', content)
        self.assertIn('isoValue0.1', content)
        self.assertIn('interpolate', content)
        self.assertIn('fields', content)

    def test_yplus(self):
        yplus = SystemDir.YPlus(self.properties)

        content = yplus.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('yPlus', content)
        self.assertIn('typeyPlus;', content)
        self.assertIn('libs(fieldFunctionObjects);', content)
        self.assertIn('writeControl', content)
        self.assertIn('patches', content)

    def test_residuals(self):
        residuals = SystemDir.Residuals(self.properties)

        content = residuals.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('residuals', content)
        self.assertIn('typesolverInfo;', content)
        self.assertIn('libs(utilityFunctionObjects);', content)
        self.assertIn('fields(".*")', content)

    def test_mach_number(self):
        mach_number = SystemDir.MachNumber(self.properties)

        content = mach_number.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('MachNo', content)
        self.assertIn('typeMachNo;', content)
        self.assertIn('libs(fieldFunctionObjects);', content)
        self.assertIn('writeControlwriteTime;', content)

    def test_surface_feature_extract(self):
        surf_extract = SystemDir.SurfaceFeatureExtract(self.properties)

        content = surf_extract.get_file_content()
        content = content.replace(' ', '').replace('\t', '').replace('\n', '')

        self.assertIn('surfaceFeatureExtractDict', content)
        self.assertIn('extractionMethod', content)
        self.assertIn('includedAngle', content)
        self.assertIn('subsetFeatures', content)
        self.assertIn('nonManifoldEdges', content)
        self.assertIn('openEdges', content)
        self.assertIn('writeObj', content)
