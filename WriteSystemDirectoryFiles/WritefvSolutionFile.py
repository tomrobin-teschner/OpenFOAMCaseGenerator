import GlobalVariables as Parameters

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
        self.file_manager.write(file_id, '        solver           GAMG;\n')
        self.file_manager.write(file_id, '        smoother         FDIC;\n')
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
        self.file_manager.write(file_id, '    "(U|k|omega|epsilon|nuTilda|q|zeta|ReThetat|gammaInt|kl|kt|R)"\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        solver           PBiCGStab;\n')
        self.file_manager.write(file_id, '        preconditioner   DILU;\n')
        self.file_manager.write(file_id, '        tolerance        ' + str(
            self.properties['convergence_control']['absolute_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '        relTol           ' + str(
            self.properties['convergence_control']['relative_convergence_criterion']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    "(UFinal|kFinal|omegaFinal|epsilonFinal|nuTildaFinal|qFinal|ReThetatFinal|gammaIntFinal|klFinal|ktFinal|RFinal)"\n')
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
        self.file_manager.write(file_id, '    nNonOrthogonalCorrectors   2;\n')
        self.file_manager.write(file_id, '    pRefCell                   0;\n')
        self.file_manager.write(file_id, '    pRefValue                  0;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    residualControl\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        U         ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        p         ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        k         ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        omega     ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        epsilon   ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        nuTilda   ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        Rethetat  ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        gammaInt  ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        kl        ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        kt        ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '        R         ' +
                                str(self.properties['convergence_control']['convergence_threshold']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'relaxationFactors\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    fields\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        p         ' +
                                str(self.properties['solver_properties']['under_relaxation_p']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    equations\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        U         ' +
                                str(self.properties['solver_properties']['under_relaxation_U']) + ';\n')
        self.file_manager.write(file_id, '        k         ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        omega     ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        epsilon   ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        nuTilda   ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        ReThetat  ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        gammaInt  ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        kl        ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        kt        ' +
                                str(self.properties['solver_properties']['under_relaxation_turbulence']) + ';\n')
        self.file_manager.write(file_id, '        R         ' +
                                str(self.properties['solver_properties']['under_relaxation_reynolds_stresses']) + ';\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
