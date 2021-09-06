import sys
import warnings
from input import GlobalVariables as Parameters


class CheckCase:
    def __init__(self, properties):
        self.properties = properties

    def run_all_checks(self):
        self.check_correct_turbulence_model_setup()
        self.check_correct_time_stepping_setup()
        self.check_correct_boundary_condition_setup()
        self.check_appropriate_numerical_scheme_combination()
        self.check_appropriate_pressure_solver()
        self.check_correct_incompressible_solver_setup()
        self.check_correct_compressible_solver_setup()

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
                     'which requires an unsteady solver instead. It is recommended switching to the\n' +
                     'pimpleFoam solver here.\n' +
                     '\n=================================== END ERROR ===================================\n')

        if (self.properties['solver_properties']['solver'] == Parameters.rhoSimpleFoam and
                self.properties['turbulence_properties']['turbulence_type'] == Parameters.LES):
            sys.exit('\n===================================== ERROR =====================================\n' +
                     '\nrhoSimpleFoam may only be used for steady state calculations but LES is selected\n' +
                     'which requires an unsteady solver instead. It is recommended switching to the\n' +
                     'rhoPimpleFoam solver here.\n' +
                     '\n=================================== END ERROR ===================================\n')

    def check_correct_time_stepping_setup(self):
        if ((self.properties['solver_properties']['solver'] == Parameters.simpleFoam and
                self.properties['numerical_discretisation']['time_integration'] == Parameters.UNSTEADY) or
            (self.properties['solver_properties']['solver'] == Parameters.rhoSimpleFoam and
                self.properties['numerical_discretisation']['time_integration'] == Parameters.UNSTEADY)):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected an unsteady discretisation but are using a steady state solver.\n' +
                'Double check that your setup is correct and either select a unsteady solver\n' +
                '(i.e. non SIMPLE based) or switch to a steady state discretisation.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)

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
        if (self.properties['numerical_discretisation']['numerical_schemes_correction'] != Parameters.ACCURACY and
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

    def check_appropriate_pressure_solver(self):
        if (self.properties['parallel_properties']['run_in_parallel'] == True and
                self.properties['solver_properties']['pressure_solver'] == Parameters.MULTI_GRID):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected to solve the pressure field with a multigrid solver and at the\n' +
                'same time you have selected to run the case in parallel. Parallel efficiency may be \n' +
                'reduced in this case and a (preconditioned) conjugate gradient method is recommened.\n' +
                'You can set the pressure solver to KRYLOV to select a conjugate gradient approach.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)

    def check_correct_incompressible_solver_setup(self):
        solver = self.properties['solver_properties']['solver']
        flow_type = self.properties['flow_properties']['flow_type']
        if (flow_type == Parameters.incompressible) and (solver == Parameters.rhoCentralFoam or
                                                         solver == Parameters.rhoSimpleFoam or
                                                         solver == Parameters.rhoPimpleFoam or
                                                         solver == Parameters.sonicFoam):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected the fluid to be incompressible but have selected a compressible\n' +
                'solver. You should either change the flow type or the solver. Only continue if you \n' +
                'know what you are doing and are sure your setup is correct.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)

    def check_correct_compressible_solver_setup(self):
        solver = self.properties['solver_properties']['solver']
        flow_type = self.properties['flow_properties']['flow_type']
        if (flow_type == Parameters.compressible) and (solver == Parameters.simpleFoam or
                                                       solver == Parameters.pimpleFoam or
                                                       solver == Parameters.icoFoam or
                                                       solver == Parameters.pisoFoam):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected the fluid to be compressible but have selected an incompressible\n' +
                'solver. You should either change the flow type or the solver. Only continue if you \n' +
                'know what you are doing and are sure your setup is correct.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)
