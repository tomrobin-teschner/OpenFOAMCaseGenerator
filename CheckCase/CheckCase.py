import sys, warnings
import GlobalVariables as Parameters


class CheckCase:
    def __init__(self, properties):
        self.properties = properties

    def check_correct_turbulence_model_setup(self):
        if (self.properties['turbulence_properties']['RANS_model'] == Parameters.kOmegaSSTLM or
                self.properties['turbulence_properties']['RANS_model'] == Parameters.kkLOmega):
            if self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nTransition models can not be run with wall functions and require a mesh\n' +
                         'resolution of y+<1. Ensure that the mesh\'s resolution is fine enough and select\n' +
                         'a low-Re wall modelling approach here.\n' +
                         '\n=================================== END ERROR ===================================\n')

        if self.properties['turbulence_properties']['RANS_model'] == Parameters.SpalartAllmaras:
            if self.properties['turbulence_properties']['wall_modelling'] == Parameters.HIGH_RE:
                warnings.showwarning(
                    '\n==================================== WARNING ====================================\n' +
                    '\nStandard Spalart-Allmaras RANS model should be run with y+<1. Using y+>30 may\n' +
                    'work, but you should consider either increasing the mesh resolution or switching\n' +
                    'your turbulence model to a high-Re approach (k-omega SST is recommended here).\n' +
                    '\n================================== END WARNING ==================================\n',
                    UserWarning, '', 0)

        if (self.properties['solver_properties']['solver'] == Parameters.simpleFoam and
                self.properties['turbulence_properties']['turbulence_type'] == Parameters.LES):
            sys.exit('\n===================================== ERROR =====================================\n' +
                     '\nsimpleFoam may only be used for steady state calculations but LES is selected\n' +
                     'which requires and unsteady solver instead. It is recommended switching to the\n' +
                     'pimpleFoam solver here.\n' +
                     '\n=================================== END ERROR ===================================\n')

    def check_correct_boundary_condition_setup(self):
        if self.properties['solver_properties']['solver'] == Parameters.simpleFoam:
            contains_advective_outlet = False
            for boundary in self.properties['boundary_properties']:
                if self.properties['boundary_properties'][boundary] == Parameters.ADVECTIVE_OUTLET:
                    contains_advective_outlet = True
            if contains_advective_outlet:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nsimpleFoam may only be used for steady state calculations but advective outlet\n' +
                         'boundary condition requires unsteady flow field. Either use inlet/outlet or neumann\n' +
                         'boundary condition or switch to an unsteady solver (pimpleFoam recommended).\n' +
                         '\n=================================== END ERROR ===================================\n')

    def check_appropriate_numerical_scheme_combination(self):
        if (self.properties['solver_properties']['numerical_schemes_correction'] != Parameters.ACCURACY and
                self.properties['turbulence_properties']['turbulence_type'] == Parameters.LES):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nRunning LES simulations should be done with accurate solver and discretisation\n' +
                'settings. Consider changing the numerical scheme policy to ACCURATE instead of the\n' +
                'current choice. You should start your simulation from an initial RANS simulation\n' +
                'which should provide enough stability. If you experience divergence, you may wish\n' +
                'to revisit your meshing approach and potential increase the mesh quality.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)
