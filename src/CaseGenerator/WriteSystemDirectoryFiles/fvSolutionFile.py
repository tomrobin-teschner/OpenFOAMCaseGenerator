from src.CaseGenerator.Properties.GlobalVariables import *
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.FileDirectoryIO import WriteHeader

class fvSolutionFile:
    def __init__(self, properties):
        self.properties = properties
        self.state_variable_manager = ZeroDir.StateVariableManager(properties)
        self.variable_names = self.state_variable_manager.get_active_variable_names()

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        fv_solution = WriteHeader.get_header(version, 'dictionary', 'system', 'fvSolution')

        abs_tol = str(self.properties['convergence_control']['absolute_convergence_criterion'])
        rel_tol = str(self.properties['convergence_control']['relative_convergence_criterion'])

        fv_solution += f'\n'
        fv_solution += f'solvers\n{{\n'

        for var in self.variable_names:
            if var == 'p':
                fv_solution += f'    p\n'
                fv_solution += f'    {{\n'
                if self.properties['solver_properties']['pressure_solver'] == PressureSolver.multi_grid:
                    fv_solution += f'        solver           GAMG;\n'
                    fv_solution += f'        smoother         FDIC;\n'
                elif self.properties['solver_properties']['pressure_solver'] == PressureSolver.krylov:
                    fv_solution += f'        solver           PCG;\n'
                    fv_solution += f'        preconditioner   FDIC;\n'
                fv_solution += f'        tolerance        ' + abs_tol + ';\n'
                fv_solution += f'        relTol           ' + rel_tol + ';\n'
                fv_solution += f'    }}\n'
                fv_solution += f'\n'
                fv_solution += f'    pFinal\n'
                fv_solution += f'    {{\n'
                fv_solution += f'        $p;\n'
                fv_solution += f'    }}\n'
                fv_solution += f'\n'
                if self.properties['flow_properties']['flow_type'] == FlowType.compressible:
                    fv_solution += f'    rho\n'
                    fv_solution += f'    {{\n'
                    if self.properties['solver_properties']['pressure_solver'] == PressureSolver.multi_grid:
                        fv_solution += f'        solver           GAMG;\n'
                        fv_solution += f'        smoother         FDIC;\n'
                    elif self.properties['solver_properties']['pressure_solver'] == PressureSolver.krylov:
                        fv_solution += f'        solver           PCG;\n'
                        fv_solution += f'        preconditioner   FDIC;\n'
                    fv_solution += f'        tolerance        ' + abs_tol + ';\n'
                    fv_solution += f'        relTol           ' + rel_tol + ';\n'
                    fv_solution += f'    }}\n'
                    fv_solution += f'\n'
                    fv_solution += f'    rhoFinal\n'
                    fv_solution += f'    {{\n'
                    fv_solution += f'        $rho;\n'
                    fv_solution += f'    }}\n'
                    fv_solution += f'\n'
                    fv_solution += f'    e\n'
                    fv_solution += f'    {{\n'
                    fv_solution += f'        solver           PBiCGStab;\n'
                    fv_solution += f'        preconditioner   DILU;\n'
                    fv_solution += f'        tolerance        {abs_tol};\n'
                    fv_solution += f'        relTol           {rel_tol};\n'
                    fv_solution += f'    }}\n'
                    fv_solution += f'\n'
                    fv_solution += f'    eFinal\n'
                    fv_solution += f'    {{\n'
                    fv_solution += f'        $e;\n'
                    fv_solution += f'    }}\n'
                    fv_solution += f'\n'
            else:
                fv_solution += f'    {var}\n'
                fv_solution += f'    {{\n'
                fv_solution += f'        solver           PBiCGStab;\n'
                fv_solution += f'        preconditioner   DILU;\n'
                fv_solution += f'        tolerance        {abs_tol};\n'
                fv_solution += f'        relTol           {rel_tol};\n'
                fv_solution += f'    }}\n'
                fv_solution += f'\n'
                fv_solution += f'    {var}Final\n'
                fv_solution += f'    {{\n'
                fv_solution += f'        ${var};\n'
                fv_solution += f'    }}\n'
                fv_solution += f'\n'
        fv_solution += f'}}\n'
        fv_solution += f'\n'
        fv_solution += f'"(SIMPLE|PISO|PIMPLE)"\n'
        fv_solution += f'{{\n'
        n_correctors = self.properties['solver_properties']['number_of_corrector_steps']
        n_outer_correctors = self.properties['solver_properties']['number_of_outer_corrector_steps']
        n_orthogonal_correctors = self.properties['solver_properties']['number_of_non_orthogonal_corrector_steps']
        if self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
            fv_solution += f'    consistent                 yes;\n'
            fv_solution += f'    nCorrectors                ' + str(n_correctors) + ';\n'
            fv_solution += f'    nOuterCorrectors           ' + str(n_outer_correctors) + ';\n'
            fv_solution += f'    nNonOrthogonalCorrectors   ' + str(n_orthogonal_correctors) + ';\n'
            fv_solution += f'    pRefCell                   0;\n'
            fv_solution += f'    pRefValue                  0;\n'
        elif self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            fv_solution += f'    consistent                 no;\n'
            fv_solution += f'    nCorrectors                ' + str(n_correctors) + ';\n'
            fv_solution += f'    nOuterCorrectors           ' + str(n_outer_correctors) + ';\n'
            fv_solution += f'    nNonOrthogonalCorrectors   ' + str(n_orthogonal_correctors) + ';\n'
            boundaries = self.properties['boundary_properties']['boundary_conditions']
            use_pressure_min_max_factors = False
            for key, value in boundaries.items():
                if ((value == BoundaryConditions.inlet) or (value == BoundaryConditions.outlet) or (value == OutletBoundaryCondition.inlet_outlet) or
                        (value == BoundaryConditions.freestream) or (value == BoundaryConditions.backflow_outlet) or
                        (value == BoundaryConditions.advective_outlet) or (value == BoundaryConditions.dfsem_inlet)):
                    use_pressure_min_max_factors = True
            if use_pressure_min_max_factors:
                fv_solution += f'    pMaxFactor                 1.5;\n'
                fv_solution += f'    pMinFactor                 0.9;\n'
            else:
                fv_solution += f'    pMax                       1;\n'
                fv_solution += f'    pMin                       1e10;\n'

        fv_solution += f'\n'
        fv_solution += f'    residualControl\n'
        fv_solution += f'    {{\n'
        if ((self.properties['solver_properties']['solver'] is Solver.simpleFoam) or
                (self.properties['solver_properties']['solver'] is Solver.rhoSimpleFoam)):
            fv_solution += f'        "(.*)"\t\t{self.properties["convergence_control"]["convergence_threshold"]};\n'
        else:
            fv_solution += f'        "(.*)"\n'
            fv_solution += f'        {{\n'
            fv_solution += f'            relTol             0;\n'
            fv_solution += f'            tolerance          '
            fv_solution += f'{self.properties["convergence_control"]["convergence_threshold"]};\n'
            fv_solution += f'        }}\n'
        fv_solution += f'    }}\n'
        fv_solution += f'}}\n'
        fv_solution += f'\n'
        fv_solution += f'relaxationFactors\n'
        fv_solution += f'{{\n'
        fv_solution += f'    fields\n'
        fv_solution += f'    {{\n'
        fv_solution += f'        "(.*)"\t\t{self.properties["solver_properties"]["under_relaxation_default"]};\n'
        for key, value in self.properties['solver_properties']['under_relaxation_fields'].items():
            fv_solution += f'        ' + key + '\t\t\t' + str(value) + ';\n'
        fv_solution += f'    }}\n'
        fv_solution += f'\n'
        fv_solution += f'    equations\n'
        fv_solution += f'    {{\n'
        fv_solution += f'        "(.*)"\t\t{self.properties["solver_properties"]["under_relaxation_default"]};\n'
        for key, value in self.properties['solver_properties']['under_relaxation_equations'].items():
            fv_solution += f'        ' + key + '\t\t\t' + str(value) + ';\n'
        fv_solution += f'    }}\n'
        fv_solution += f'}}\n'
        fv_solution += f'\n'
        fv_solution += f'// ************************************************************************* //\n'
        return fv_solution
