import unittest
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.Properties.GlobalVariables import *


class TestTurbulenceFreestreamConditions(unittest.TestCase):
    def setUp(self):
        self.properties = {}
        self.properties['file_properties'] = {}
        self.properties['flow_properties'] = {}
        self.properties['turbulence_properties'] = {}
        self.properties['dimensionless_coefficients'] = {}
        self.properties['flow_properties']['dimensional_properties'] = {}
        self.properties['flow_properties']['non_dimensional_properties'] = {}
        self.properties['file_properties']['version'] = 'v2212'
        self.properties['flow_properties']['dimensional_properties']['velocity_magnitude'] = 1.0
        self.properties['flow_properties']['dimensional_properties']['nu'] = 1e-6
        self.properties['turbulence_properties']['freestream_turbulent_intensity'] = 0.01
        self.properties['dimensionless_coefficients']['reference_length'] = 1.0
        self.properties['flow_properties']['non_dimensional_properties']['Re'] = 85000
        self.properties['turbulence_properties']['turbulent_to_laminar_ratio'] = 50

    def test_freestream_k(self):
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_k = freestream_conditions.calculate_freestream_k()
        
        self.assertAlmostEqual(freestream_k, 0.00015)

    def test_freestream_omega_internal(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.internal
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_omega = freestream_conditions.calculate_freestream_omega()

        self.assertAlmostEqual(freestream_omega, 0.31943828)

    def test_freestream_omega_external(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.external
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_omega = freestream_conditions.calculate_freestream_omega()

        self.assertAlmostEqual(freestream_omega, 1.46253770)

    def test_freestream_omega_ratio(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.ratio
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_omega = freestream_conditions.calculate_freestream_omega()

        self.assertAlmostEqual(freestream_omega, 3.0)

    def test_freestream_omega_ratio_auto(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.ratio_auto
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_omega = freestream_conditions.calculate_freestream_omega()

        self.assertAlmostEqual(freestream_omega, 150.0)

    def test_freestream_epsilon_internal(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.internal
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_epsilon = freestream_conditions.calculate_freestream_epsilon()

        self.assertAlmostEqual(freestream_epsilon, 4.31241681e-06)

    def test_freestream_epsilon_external(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.external
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_epsilon = freestream_conditions.calculate_freestream_epsilon()

        self.assertAlmostEqual(freestream_epsilon, 1.97442590e-05)

    def test_freestream_epsilon_ratio(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.ratio
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_epsilon = freestream_conditions.calculate_freestream_epsilon()

        self.assertAlmostEqual(freestream_epsilon, 4.05e-5)

    def test_freestream_epsilon_ratio_auto(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.ratio_auto
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_epsilon = freestream_conditions.calculate_freestream_epsilon()

        self.assertAlmostEqual(freestream_epsilon, 0.002025)

    def test_freestream_nuTilda_internal(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.internal
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_nuTilda = freestream_conditions.calculate_freestream_nuTilda()

        self.assertAlmostEqual(freestream_nuTilda, 0.00085732)

    def test_freestream_nuTilda_external(self):
        self.properties['turbulence_properties']['turbulent_quantities_at_inlet'] = TurbulenceLengthScaleCalculation.external
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_nuTilda = freestream_conditions.calculate_freestream_nuTilda()

        self.assertAlmostEqual(freestream_nuTilda, 0.00018725)

    def test_freestream_ReThetaT(self):
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_ReThetaT = freestream_conditions.calculate_ReThetaT()

        self.assertAlmostEqual(freestream_ReThetaT, 584.3016)

    def test_freestream_ReThetaT_high_turbulence_intensity(self):
        self.properties['turbulence_properties']['freestream_turbulent_intensity'] = 0.5
        freestream_conditions = ZeroDir.TurbulenceFreestreamConditions(self.properties)

        freestream_ReThetaT = freestream_conditions.calculate_ReThetaT()

        self.assertAlmostEqual(freestream_ReThetaT, 24.19864638)

