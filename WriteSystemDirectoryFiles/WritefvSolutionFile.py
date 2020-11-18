class fvSolutionFile:
    def __init__(self, file_manager, solver_properties):
        self.file_manager = file_manager
        self.solver_properties = solver_properties

    def write_input_file(self):
        file_id = self.file_manager.create_file('system', 'fvSolution')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fvSolution')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'solvers\n{\n')
        self.file_manager.write(file_id, '    p\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        solver           GAMG;\n')
        self.file_manager.write(file_id, '        smoother         FDIC;\n')
        self.file_manager.write(file_id, '        tolerance        ' + str(
            self.solver_properties['absolute_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '        relTol           ' + str(
            self.solver_properties['relative_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    pFinal\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        $p;\n')
        self.file_manager.write(file_id, '        relTol           0;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    "(U|k|omega|epsilon|nuTilda|zeta|ReThetat|gammaInt|R)"\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        solver           PBiCGStab;\n')
        self.file_manager.write(file_id, '        preconditioner   DILU;\n')
        self.file_manager.write(file_id, '        tolerance        ' + str(
            self.solver_properties['absolute_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '        relTol           ' + str(
            self.solver_properties['relative_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    "(UFinal|kFinal|omegaFinal|epsilonFinal|nuTildaFinal|zetaFinal|ReThetatFinal|gammaIntFinal|RFinal)"\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        $U;\n')
        self.file_manager.write(file_id, '        relTol           0;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '"(SIMPLE|PISO)"\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    consistent                 yes;\n')
        self.file_manager.write(file_id, '    nCorrectors                2;\n')
        self.file_manager.write(file_id, '    nNonOrthogonalCorrectors   0;\n')
        self.file_manager.write(file_id, '    pRefCell                   0;\n')
        self.file_manager.write(file_id, '    pRefValue                  0;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    residualControl\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id,
                                '        U         ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        p         ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        k         ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        omega     ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        epsilon   ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        nuTilda   ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        Rethetat  ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id,
                                '        gammaInt  ' + str(self.solver_properties['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'relaxationFactors\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    fields\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id,
                                '        p         ' + str(self.solver_properties['under_relaxation_p']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    equations\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id,
                                '        U         ' + str(self.solver_properties['under_relaxation_U']) + ';\n')
        self.file_manager.write(file_id,
                                '        k         ' + str(self.solver_properties['under_relaxation_turbulence']) +
                                ';\n')
        self.file_manager.write(file_id,
                                '        omega     ' + str(self.solver_properties['under_relaxation_turbulence']) +
                                ';\n')
        self.file_manager.write(file_id,
                                '        epsilon   ' + str(self.solver_properties['under_relaxation_turbulence']) +
                                ';\n')
        self.file_manager.write(file_id,
                                '        nuTilda   ' + str(self.solver_properties['under_relaxation_turbulence']) +
                                ';\n')
        self.file_manager.write(file_id,
                                '        ReThetat  ' + str(self.solver_properties['under_relaxation_turbulence']) +
                                ';\n')
        self.file_manager.write(file_id,
                                '        gammaInt  ' + str(self.solver_properties['under_relaxation_turbulence']) +
                                ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
