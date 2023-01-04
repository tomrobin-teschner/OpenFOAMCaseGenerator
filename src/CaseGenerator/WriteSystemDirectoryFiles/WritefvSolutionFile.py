from src.CaseGenerator.Properties import GlobalVariables as Parameters
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir

class fvSolutionFile:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager
        self.state_variable_manager = ZeroDir.StateVariableManager(properties)
        self.variable_names = self.state_variable_manager.get_active_variable_names()

    def write_input_file(self):
        abs_tol = str(self.properties['convergence_control']['absolute_convergence_criterion'])
        rel_tol = str(self.properties['convergence_control']['relative_convergence_criterion'])

        file_id = self.file_manager.create_file('system', 'fvSolution')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fvSolution')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'solvers\n{\n')

        for var in self.variable_names:
            if var == 'p':
                self.file_manager.write(file_id, '    p\n')
                self.file_manager.write(file_id, '    {\n')
                if self.properties['solver_properties']['pressure_solver'] == Parameters.MULTI_GRID:
                    self.file_manager.write(file_id, '        solver           GAMG;\n')
                    self.file_manager.write(file_id, '        smoother         FDIC;\n')
                elif self.properties['solver_properties']['pressure_solver'] == Parameters.KRYLOV:
                    self.file_manager.write(file_id, '        solver           PCG;\n')
                    self.file_manager.write(file_id, '        preconditioner   FDIC;\n')
                self.file_manager.write(file_id, '        tolerance        ' + abs_tol + ';\n')
                self.file_manager.write(file_id, '        relTol           ' + rel_tol + ';\n')
                self.file_manager.write(file_id, '    }\n')
                self.file_manager.write(file_id, '\n')
                self.file_manager.write(file_id, '    pFinal\n')
                self.file_manager.write(file_id, '    {\n')
                self.file_manager.write(file_id, '        $p;\n')
                self.file_manager.write(file_id, '    }\n')
                self.file_manager.write(file_id, '\n')
                if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
                    self.file_manager.write(file_id, '    rho\n')
                    self.file_manager.write(file_id, '    {\n')
                    if self.properties['solver_properties']['pressure_solver'] == Parameters.MULTI_GRID:
                        self.file_manager.write(file_id, '        solver           GAMG;\n')
                        self.file_manager.write(file_id, '        smoother         FDIC;\n')
                    elif self.properties['solver_properties']['pressure_solver'] == Parameters.KRYLOV:
                        self.file_manager.write(file_id, '        solver           PCG;\n')
                        self.file_manager.write(file_id, '        preconditioner   FDIC;\n')
                    self.file_manager.write(file_id, '        tolerance        ' + abs_tol + ';\n')
                    self.file_manager.write(file_id, '        relTol           ' + rel_tol + ';\n')
                    self.file_manager.write(file_id, '    }\n')
                    self.file_manager.write(file_id, '\n')
                    self.file_manager.write(file_id, '    rhoFinal\n')
                    self.file_manager.write(file_id, '    {\n')
                    self.file_manager.write(file_id, '        $rho;\n')
                    self.file_manager.write(file_id, '    }\n')
                    self.file_manager.write(file_id, '\n')
            else:
                self.file_manager.write(file_id, '    ' + var + '\n')
                self.file_manager.write(file_id, '    {\n')
                self.file_manager.write(file_id, '        solver           PBiCGStab;\n')
                self.file_manager.write(file_id, '        preconditioner   DILU;\n')
                self.file_manager.write(file_id, '        tolerance        ' + abs_tol + ';\n')
                self.file_manager.write(file_id, '        relTol           ' + rel_tol + ';\n')
                self.file_manager.write(file_id, '    }\n')
                self.file_manager.write(file_id, '\n')
                self.file_manager.write(file_id, '    ' + var + 'Final\n')
                self.file_manager.write(file_id, '    {\n')
                self.file_manager.write(file_id, '        $' + var + ';\n')
                self.file_manager.write(file_id, '    }\n')
                self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '"(SIMPLE|PISO|PIMPLE)"\n')
        self.file_manager.write(file_id, '{\n')
        n_correctors = self.properties['solver_properties']['number_of_corrector_steps']
        n_outer_correctors = self.properties['solver_properties']['number_of_outer_corrector_steps']
        n_orthogonal_correctors = self.properties['solver_properties']['number_of_non_orthogonal_corrector_steps']
        if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            self.file_manager.write(file_id, '    consistent                 yes;\n')
            self.file_manager.write(file_id, '    nCorrectors                ' + str(n_correctors) + ';\n')
            self.file_manager.write(file_id, '    nOuterCorrectors           ' + str(n_outer_correctors) + ';\n')
            self.file_manager.write(file_id, '    nNonOrthogonalCorrectors   ' + str(n_orthogonal_correctors) + ';\n')
            self.file_manager.write(file_id, '    pRefCell                   0;\n')
            self.file_manager.write(file_id, '    pRefValue                  0;\n')
        elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.file_manager.write(file_id, '    consistent                 no;\n')
            self.file_manager.write(file_id, '    nCorrectors                ' + str(n_correctors) + ';\n')
            self.file_manager.write(file_id, '    nOuterCorrectors           ' + str(n_outer_correctors) + ';\n')
            self.file_manager.write(file_id, '    nNonOrthogonalCorrectors   ' + str(n_orthogonal_correctors) + ';\n')
            boundaries = self.properties['boundary_properties']['boundary_conditions']
            use_pressure_min_max_factors = False
            for key, value in boundaries.items():
                if ((value == Parameters.INLET) or (value == Parameters.OUTLET) or (value == Parameters.INLET_OUTLET) or
                        (value == Parameters.FREESTREAM) or (value == Parameters.BACKFLOW_OUTLET) or
                        (value == Parameters.ADVECTIVE_OUTLET) or (value == Parameters.DFSEM_INLET)):
                    use_pressure_min_max_factors = True
            if use_pressure_min_max_factors:
                self.file_manager.write(file_id, '    pMaxFactor                 1.5;\n')
                self.file_manager.write(file_id, '    pMinFactor                 0.9;\n')
            else:
                self.file_manager.write(file_id, '    pMax                       1;\n')
                self.file_manager.write(file_id, '    pMin                       1e10;\n')

        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    residualControl\n')
        self.file_manager.write(file_id, '    {\n')
        if ((self.properties['solver_properties']['solver'] is Parameters.simpleFoam) or
                (self.properties['solver_properties']['solver'] is Parameters.rhoSimpleFoam)):
            self.file_manager.write(file_id, '        "(.*)"\t\t' +
                                    str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        else:
            self.file_manager.write(file_id, '        "(.*)"\n')
            self.file_manager.write(file_id, '        {\n')
            self.file_manager.write(file_id, '            relTol             0;\n')
            self.file_manager.write(file_id, '            tolerance          ')
            self.file_manager.write(file_id, str(self.properties['convergence_control']['convergence_threshold']) +
                                    ';\n')
            self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'relaxationFactors\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    fields\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        "(.*)"\t\t' +
                                str(self.properties['solver_properties']['under_relaxation_default']) + ';\n')
        for key, value in self.properties['solver_properties']['under_relaxation_fields'].items():
            self.file_manager.write(file_id, '        ' + key + '\t\t\t' + str(value) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    equations\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        "(.*)"\t\t' +
                                str(self.properties['solver_properties']['under_relaxation_default']) + ';\n')
        for key, value in self.properties['solver_properties']['under_relaxation_equations'].items():
            self.file_manager.write(file_id, '        ' + key + '\t\t\t' + str(value) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
