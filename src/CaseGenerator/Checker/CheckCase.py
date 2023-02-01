import sys
import warnings
from src.CaseGenerator.Properties.GlobalVariables import *


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
        self.check_sensible_convergence_criterion()
        self.check_force_coefficients()

    def check_correct_turbulence_model_setup(self):
        rans_model = self.properties['turbulence_properties']['RansModel']
        if (rans_model == RansModel.kOmegaSSTLM or
                rans_model == RansModel.kkLOmega):
            if self.properties['turbulence_properties']['wall_modelling'] == WallModelling.high_re:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nTransition models can not be run with wall functions and require a mesh\n' +
                         'resolution of y+<1. Ensure that the mesh\'s resolution is fine enough and select\n' +
                         'a low-Re wall modelling approach here.\n' +
                         '\n=================================== END ERROR ===================================\n')

        if rans_model == RansModel.SpalartAllmaras:
            if self.properties['turbulence_properties']['wall_modelling'] == WallModelling.high_re:
                warnings.showwarning(
                    '\n==================================== WARNING ====================================\n' +
                    '\nStandard Spalart-Allmaras RANS model should be run with y+<1. Using y+>30 may\n' +
                    'work, but you should consider either increasing the mesh resolution or switching\n' +
                    'your turbulence model to a high-Re approach (k-omega SST is recommended here).\n' +
                    '\n================================== END WARNING ==================================\n',
                    UserWarning, '', 0)

        if (self.properties['solver_properties']['solver'] == Solver.simpleFoam and
                self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.les):
            sys.exit('\n===================================== ERROR =====================================\n' +
                     '\nsimpleFoam may only be used for steady state calculations but LES is selected\n' +
                     'which requires an unsteady solver instead. It is recommended switching to the\n' +
                     'pimpleFoam solver here.\n' +
                     '\n=================================== END ERROR ===================================\n')

        if (self.properties['solver_properties']['solver'] == Solver.rhoSimpleFoam and
                self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.les):
            sys.exit('\n===================================== ERROR =====================================\n' +
                     '\nrhoSimpleFoam may only be used for steady state calculations but LES is selected\n' +
                     'which requires an unsteady solver instead. It is recommended switching to the\n' +
                     'rhoPimpleFoam solver here.\n' +
                     '\n=================================== END ERROR ===================================\n')

    def check_correct_time_stepping_setup(self):
        if ((self.properties['solver_properties']['solver'] == Solver.simpleFoam and
                self.properties['time_discretisation']['time_integration'] == TimeTreatment.unsteady) or
            (self.properties['solver_properties']['solver'] == Solver.rhoSimpleFoam and
                self.properties['time_discretisation']['time_integration'] == TimeTreatment.unsteady)):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected an unsteady discretisation but are using a steady state solver.\n' +
                'Double check that your setup is correct and either select a unsteady solver\n' +
                '(i.e. non SIMPLE based) or switch to a steady state discretisation.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)

    def check_correct_boundary_condition_setup(self):
        if self.properties['solver_properties']['solver'] == Solver.simpleFoam:
            contains_advective_outlet = False
            for boundary in self.properties['boundary_properties']:
                if self.properties['boundary_properties'][boundary] == BoundaryConditions.advective_outlet:
                    contains_advective_outlet = True
            if contains_advective_outlet:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nsimpleFoam may only be used for steady state calculations but advective outlet\n' +
                         'boundary condition requires unsteady flow field. Either use inlet/outlet or neumann\n' +
                         'boundary condition or switch to an unsteady solver (pimpleFoam recommended).\n' +
                         '\n=================================== END ERROR ===================================\n')

    def check_appropriate_numerical_scheme_combination(self):
        if (self.properties['spatial_discretisation']['numerical_schemes_correction'] != DiscretisationPolicy.accuracy
                and self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.les):
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
                self.properties['solver_properties']['pressure_solver'] == PressureSolver.multi_grid):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected to solve the pressure field with a multigrid solver and at the\n' +
                'same time you have selected to run the case in parallel. Parallel efficiency may be \n' +
                'reduced in this case and a (preconditioned) conjugate gradient method is recommened.\n' +
                'You can set the pressure solver to krylov to select a conjugate gradient approach.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)

    def check_correct_incompressible_solver_setup(self):
        solver = self.properties['solver_properties']['solver']
        flow_type = self.properties['flow_properties']['flow_type']
        equation = self.properties['flow_properties']['equations']
        if (flow_type == FlowType.incompressible) and (solver == Solver.rhoCentralFoam or
                                                       solver == Solver.rhoSimpleFoam or
                                                       solver == Solver.rhoPimpleFoam or
                                                       solver == Solver.sonicFoam):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected the fluid to be incompressible but have selected a compressible\n' +
                'solver. You should either change the flow type or the solver. Only continue if you \n' +
                'know what you are doing and are sure your setup is correct.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)
        
        if flow_type == FlowType.incompressible and equation == Equations.euler:
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou are solving the inviscid and incompressible Navier-Stokes equations which have\n' +
                'no practical application. Unless you know what you are doing, you probably want to\n' +
                'change the equation to Equations.navier_stokes instead of Equations.euler!\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)

    def check_correct_compressible_solver_setup(self):
        solver = self.properties['solver_properties']['solver']
        flow_type = self.properties['flow_properties']['flow_type']
        turbulence_type = self.properties['turbulence_properties']['turbulence_type']
        les_model = self.properties['turbulence_properties']['LesModel']
        if (flow_type == FlowType.compressible) and (solver == Solver.simpleFoam or
                                                     solver == Solver.pimpleFoam or
                                                     solver == Solver.icoFoam or
                                                     solver == Solver.pisoFoam):
            warnings.showwarning(
                '\n==================================== WARNING ====================================\n' +
                '\nYou have selected the fluid to be compressible but have selected an incompressible\n' +
                'solver. You should either change the flow type or the solver. Only continue if you \n' +
                'know what you are doing and are sure your setup is correct.\n' +
                '\n================================== END WARNING ==================================\n',
                UserWarning, '', 0)
        if (flow_type == FlowType.compressible) and (turbulence_type == TurbulenceType.les):
            if les_model == LesModel.DeardorffDiffStress:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nRunning Compressible flow with DeardorffDiffStress as the LES sub-grid scale model\n' +
                         'will result in a strange error (it seems the equations expect the Reynolds stresses\n' +
                         'to have different dimensions in different equations). This should work, but there\n' +
                         'does not seem to be any documentation, nor tutorials, nor other resources available\n' +
                         'that could show how to deal with this sub-grid scale mode. If you know what you are\n' +
                         'doing and want to continue, run the case generator with the --no-checks option\n' +
                         'to generate a case. Should you be able to get the compressible version of the\n' +
                         'DeardorffDiffStress model to work, I\'d be grateful for you to leave a comment at:\n' +
                         'https://www.cfd-online.com/Forums/openfoam-solving/247285-les-deardorffdiffstress.html\n' +
                         '\n=================================== END ERROR ===================================\n')

    def check_sensible_convergence_criterion(self):
        unsteady = self.properties['time_discretisation']['time_integration']
        abs_tol = self.properties['convergence_control']['absolute_convergence_criterion']
        rel_tol = self.properties['convergence_control']['relative_convergence_criterion']
        if unsteady:
            if abs_tol > 1e-4:
                warnings.showwarning(
                    '\n==================================== WARNING ====================================\n' +
                    '\nYou are running an unsteady case but your absolute convergence criterion for the\n' +
                    'implicit system of equations is too high and is likely to cause diffusion in time\n' +
                    'and thus inaccurate results. Consider lowering your absolute convergence criterion.\n' +
                    '\nCurrent absolute convergence criterion    : ' + str(abs_tol) + '\n' +
                    'Recommended absolute convergence criterion: 1e-4 (or lower)\n' +
                    '\n================================== END WARNING ==================================\n',
                    UserWarning, '', 0)
            if rel_tol > 1e-4:
                warnings.showwarning(
                    '\n==================================== WARNING ====================================\n' +
                    '\nYou are running an unsteady case but your relative convergence criterion for the\n' +
                    'implicit system of equations is too high and is likely to cause diffusion in time\n' +
                    'and thus inaccurate results. Consider lowering your relative convergence criterion.\n' +
                    '\nCurrent relative convergence criterion    : ' + str(rel_tol) + '\n' +
                    'Recommended relative convergence criterion: 1e-4 (or lower)\n' +
                    '\n================================== END WARNING ==================================\n',
                    UserWarning, '', 0)

    def check_force_coefficients(self):
        force_coefficient_writing_active = self.properties['dimensionless_coefficients']['write_force_coefficients']
        boundary_conditions = self.properties['boundary_properties']['boundary_conditions']
        wall_patches = self.properties['dimensionless_coefficients']['wall_boundaries']

        if force_coefficient_writing_active:
            if len(wall_patches) == 0:
                sys.exit('\n===================================== ERROR =====================================\n' +
                         '\nForce coefficient calculation is requested, but no boundary patches are specified,\n' +
                         'within the properties[\'dimensionless_coefficients\'][\'wall_boundaries\'] dictionary.\n' +
                         'Ensure you specify the wall patches at which forces should be calculated.\n' +
                         '\n=================================== END ERROR ===================================\n')

            for patch in wall_patches:
                if patch not in boundary_conditions:
                    sys.exit('\n===================================== ERROR =====================================\n' +
                             '\nThe boundary condition \'' + patch + '\' was not found in the\n' +
                             'boundary conditions and thus may lead to unwanted force calculations. OpenFOAM may\n' +
                             'fail silently here, check your boundary conditions and wall patches at which to\n' +
                             'calculate the force coefficients again.\n' +
                             '\n=================================== END ERROR ===================================\n')

                if boundary_conditions[patch] is not BoundaryConditions.wall:
                    sys.exit('\n===================================== ERROR =====================================\n' +
                             '\nThe boundary condition \'' + patch + '\' was found in the\n' +
                             'boundary conditions but is not of wall type. Check your boundary conditions and \n' +
                             'wall patches at which to calculate the force coefficients again.\n' +
                             '\n=================================== END ERROR ===================================\n')
