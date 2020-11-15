import GlobalVariables as Parameters


class fvSchemesFile:
    def __init__(self, file_manager, solver_properties):
        self.file_manager = file_manager
        self.solver_properties = solver_properties

    def write_input_file(self):
        stabilisation = ''
        if (self.solver_properties['numerical_schemes_correction'] == Parameters.MODERATE_CORRECTION or
            self.solver_properties['numerical_schemes_correction'] == Parameters.FULL_CORRECTION):
            stabilisation = 'bounded '

        file_id = self.file_manager.create_file('system', 'fvSchemes')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fvSchemes')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'ddtSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.solver_properties['time_integration'] == Parameters.STEADY_STATE:
            self.file_manager.write(file_id, '    default         steadyState;\n')
        elif self.solver_properties['time_integration'] == Parameters.FIRST_ORDER:
            self.file_manager.write(file_id, '    default         Euler;\n')
        elif self.solver_properties['time_integration'] == Parameters.SECOND_ORDER:
            self.file_manager.write(file_id, '    default         backward;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'gradSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.solver_properties['numerical_schemes_correction'] == Parameters.NO_CORRECTION:
            self.file_manager.write(file_id, '    default         Gauss linear;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.SLIGHT_CORRECTION:
            self.file_manager.write(file_id, '    default         cellLimited Gauss linear 0.33;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.MODERATE_CORRECTION:
            self.file_manager.write(file_id, '    default         cellLimited Gauss linear 0.5;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.FULL_CORRECTION:
            self.file_manager.write(file_id, '    default         cellLimited Gauss linear 1;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'divSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.solver_properties['turbulent_fluxes'] == Parameters.FIRST_ORDER:
            self.file_manager.write(file_id, '    default         ' + stabilisation + 'Gauss upwind grad(U);\n')
        elif self.solver_properties['turbulent_fluxes'] == Parameters.SECOND_ORDER:
            self.file_manager.write(file_id, '    default         ' + stabilisation + 'Gauss linearUpwind grad(U);\n')
        elif self.solver_properties['turbulent_fluxes'] == Parameters.THIRD_ORDER:
            self.file_manager.write(file_id, '    default         ' + stabilisation + 'Gauss MUSCL;\n')
        if self.solver_properties['convective_fluxes'] == Parameters.FIRST_ORDER:
            self.file_manager.write(file_id, '    div(phi,U)      ' + stabilisation + 'Gauss upwind grad(U);\n')
        elif self.solver_properties['convective_fluxes'] == Parameters.SECOND_ORDER:
            self.file_manager.write(file_id, '    div(phi,U)      ' + stabilisation + 'Gauss linearUpwind grad(U);\n')
        elif self.solver_properties['convective_fluxes'] == Parameters.THIRD_ORDER:
            self.file_manager.write(file_id, '    div(phi,U)      ' + stabilisation + 'Gauss MUSCL;\n')
        self.file_manager.write(file_id, '    div((nuEff*dev2(T(grad(U))))) Gauss linear;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'laplacianSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.solver_properties['numerical_schemes_correction'] == Parameters.NO_CORRECTION:
            self.file_manager.write(file_id, '    default         Gauss linear orthogonal;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.SLIGHT_CORRECTION:
            self.file_manager.write(file_id, '    default         Gauss linear limited corrected 0.33;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.MODERATE_CORRECTION:
            self.file_manager.write(file_id, '    default         Gauss linear limited corrected 0.5;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.FULL_CORRECTION:
            self.file_manager.write(file_id, '    default         Gauss linear limited corrected 1;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'interpolationSchemes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    default         linear;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'snGradSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.solver_properties['numerical_schemes_correction'] == Parameters.NO_CORRECTION:
            self.file_manager.write(file_id, '    default         orthogonal;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.SLIGHT_CORRECTION:
            self.file_manager.write(file_id, '    default         limited corrected 0.33;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.MODERATE_CORRECTION:
            self.file_manager.write(file_id, '    default         limited corrected 0.5;\n')
        elif self.solver_properties['numerical_schemes_correction'] == Parameters.FULL_CORRECTION:
            self.file_manager.write(file_id, '    default         limited corrected 1;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'wallDist\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    method          meshWave;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
