from src.CaseGenerator.Properties.GlobalVariables import *
from math import pow, sqrt


class TurbulenceFreestreamConditions:
    def __init__(self, properties):
        self.properties = properties

    def calculate_freestream_k(self):
        velocity_magnitude = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']
        turbulence_intensity = self.properties['turbulence_properties']['freestream_turbulent_intensity']
        return 1.5 * pow(velocity_magnitude * turbulence_intensity, 2)

    def calculate_freestream_omega(self):
        turbulence_at_inlet = self.properties['turbulence_properties']['turbulent_quantities_at_inlet']
        turbulent_length_scale_internal = self.__calculate_turbulent_length_scale_for_internal_flows()
        turbulent_length_scale_external = self.__calculate_turbulent_length_scale_for_external_flows()
        turbulent_to_laminar_viscosity_ratio = self.properties['turbulence_properties']['turbulent_to_laminar_ratio']
        turbulent_to_laminar_viscosity_ratio_calculated = self.__calculate_turbulent_to_laminar_viscosity_ratio()
        nu = self.properties['flow_properties']['dimensional_properties']['material_properties']['nu']
        k = self.calculate_freestream_k()

        if turbulence_at_inlet == TurbulenceLengthScaleCalculation.internal:
            return pow(ClosureCoefficients.c_mu.value, -0.25) * pow(k, 0.5) / turbulent_length_scale_internal
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.external:
            return pow(ClosureCoefficients.c_mu.value, -0.25) * pow(k, 0.5) / turbulent_length_scale_external
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.ratio:
            return (k / nu) / turbulent_to_laminar_viscosity_ratio
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.ratio_auto:
            return (k / nu) / turbulent_to_laminar_viscosity_ratio_calculated

    def calculate_freestream_epsilon(self):
        turbulence_at_inlet = self.properties['turbulence_properties']['turbulent_quantities_at_inlet']
        turbulent_length_scale_internal = self.__calculate_turbulent_length_scale_for_internal_flows()
        turbulent_length_scale_external = self.__calculate_turbulent_length_scale_for_external_flows()
        turbulent_to_laminar_viscosity_ratio = self.properties['turbulence_properties']['turbulent_to_laminar_ratio']
        turbulent_to_laminar_viscosity_ratio_calculated = self.__calculate_turbulent_to_laminar_viscosity_ratio()
        nu = self.properties['flow_properties']['dimensional_properties']['material_properties']['nu']
        k = self.calculate_freestream_k()

        if turbulence_at_inlet == TurbulenceLengthScaleCalculation.internal:
            return pow(ClosureCoefficients.c_mu.value, 0.75) * pow(k, 1.5) / turbulent_length_scale_internal
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.external:
            return pow(ClosureCoefficients.c_mu.value, 0.75) * pow(k, 1.5) / turbulent_length_scale_external
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.ratio:
            return (ClosureCoefficients.c_mu.value * pow(k, 2) / nu) / turbulent_to_laminar_viscosity_ratio
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.ratio_auto:
            return (ClosureCoefficients.c_mu.value * pow(k, 2) / nu) / turbulent_to_laminar_viscosity_ratio_calculated

    def calculate_freestream_nuTilda(self):
        turbulence_at_inlet = self.properties['turbulence_properties']['turbulent_quantities_at_inlet']
        nu = self.properties['flow_properties']['dimensional_properties']['material_properties']['nu']
        turbulent_length_scale_internal = self.__calculate_turbulent_length_scale_for_internal_flows()
        turbulent_length_scale_external = self.__calculate_turbulent_length_scale_for_external_flows()
        turbulence_intensity = self.properties['turbulence_properties']['freestream_turbulent_intensity']
        velocity_magnitude = self.properties['flow_properties']['dimensional_properties']['velocity_magnitude']

        if turbulence_at_inlet == TurbulenceLengthScaleCalculation.internal:
            return sqrt(1.5) * velocity_magnitude * turbulence_intensity * turbulent_length_scale_internal
        elif turbulence_at_inlet == TurbulenceLengthScaleCalculation.external:
            return sqrt(1.5) * velocity_magnitude * turbulence_intensity * turbulent_length_scale_external
        else:
            return 5 * nu

    def calculate_ReThetaT(self):
        turbulence_intensity = self.properties['turbulence_properties']['freestream_turbulent_intensity']
        if turbulence_intensity <= 0.013:
            return 1173.51 - 589.428 * turbulence_intensity * 100 + 0.2196 / pow(turbulence_intensity * 100, 2)
        elif turbulence_intensity > 0.013:
            return 331.5 / pow((turbulence_intensity * 100 - 0.5658), 0.671)

    def __calculate_turbulent_length_scale_for_internal_flows(self):
        return 0.07 * self.properties['dimensionless_coefficients']['reference_length']

    def __calculate_turbulent_length_scale_for_external_flows(self):
        reynolds_number = self.properties['flow_properties']['non_dimensional_properties']['Re']
        reference_length = self.properties['dimensionless_coefficients']['reference_length']
        delta = 0.37 * reference_length / pow(reynolds_number, 0.2)
        return 0.4 * delta

    def __calculate_turbulent_to_laminar_viscosity_ratio(self):
        turbulence_intensity = self.properties['turbulence_properties']['freestream_turbulent_intensity']
        if turbulence_intensity < 0.01:
            return 1
        elif 0.01 <= turbulence_intensity < 0.05:
            return 1 + 9 * (turbulence_intensity - 0.01) / 0.04
        elif 0.05 <= turbulence_intensity < 0.1:
            return 10 + 90 * (turbulence_intensity - 0.05) / 0.05
        elif turbulence_intensity >= 0.1:
            return 100
