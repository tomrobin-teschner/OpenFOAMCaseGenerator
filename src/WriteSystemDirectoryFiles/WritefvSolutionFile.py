from input import GlobalVariables as Parameters


class fvSolutionFile:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_input_file(self):
        file_id = self.file_manager.create_file('system', 'fvSolution')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fvSolution')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'solvers\n{\n')
        self.file_manager.write(file_id, '    p\n')
        self.file_manager.write(file_id, '    {\n')
        if self.properties['solver_properties']['pressure_solver'] == Parameters.MULTI_GRID:
            self.file_manager.write(file_id, '        solver           GAMG;\n')
            self.file_manager.write(file_id, '        smoother         FDIC;\n')
        elif self.properties['solver_properties']['pressure_solver'] == Parameters.KRYLOV:
            self.file_manager.write(file_id, '        solver           PCG;\n')
            self.file_manager.write(file_id, '        preconditioner   FDIC;\n')
        self.file_manager.write(file_id, '        tolerance        ' + str(
            self.properties['convergence_control']['absolute_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '        relTol           ' + str(
            self.properties['convergence_control']['relative_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    pFinal\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        $p;\n')
        self.file_manager.write(file_id, '        relTol           0;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '    "(U|T|e|rho|rhoU|k|omega|epsilon|nuTilda|q|zeta|ReThetat|gammaInt|kl|kt|R)"\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        solver           PBiCGStab;\n')
        self.file_manager.write(file_id, '        preconditioner   DILU;\n')
        self.file_manager.write(file_id, '        tolerance        ' + str(
            self.properties['convergence_control']['absolute_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '        relTol           ' + str(
            self.properties['convergence_control']['relative_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '    "(U|T|e|rho|rhoU|k|omega|epsilon|nuTilda|q|zeta|ReThetat|gammaInt|kl|kt|R)Final"\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        $U;\n')
        self.file_manager.write(file_id, '        relTol           0;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '"(SIMPLE|PISO|PIMPLE)"\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            self.file_manager.write(file_id, '    consistent                 yes;\n')
            self.file_manager.write(file_id, '    nCorrectors                2;\n')
            self.file_manager.write(file_id, '    nNonOrthogonalCorrectors   2;\n')
            self.file_manager.write(file_id, '    pRefCell                   0;\n')
            self.file_manager.write(file_id, '    pRefValue                  0;\n')
        elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.file_manager.write(file_id, '    consistent                 no;\n')
            self.file_manager.write(file_id, '    nCorrectors                2;\n')
            self.file_manager.write(file_id, '    nNonOrthogonalCorrectors   0;\n')
            self.file_manager.write(file_id, '    pMaxFactor                 1.5;\n')
            self.file_manager.write(file_id, '    pMinFactor                 0.9;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    residualControl\n')
        self.file_manager.write(file_id, '    {\n')
        if self.properties['solver_properties']['solver'] is Parameters.simpleFoam:
            self.file_manager.write(file_id, '        "(.*)"    ' +
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
