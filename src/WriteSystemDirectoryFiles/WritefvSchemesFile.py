from src import GlobalVariables as Parameters


class fvSchemesFile:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_input_file(self):
        # gradient reconstruction scheme to be used in divergence schemes, depends on turbulence model
        gradient_scheme = 'default'
        if self.properties['turbulence_properties']['use_phi_instead_of_grad_U']:
            gradient_scheme = 'phi'

        file_id = self.file_manager.create_file('system', 'fvSchemes')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fvSchemes')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'ddtSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['numerical_discretisation']['time_integration'] == Parameters.STEADY_STATE:
            self.file_manager.write(file_id, '    default         steadyState;\n')
        else:
            if self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
                self.file_manager.write(file_id, '    default         CrankNicolson 0.5;\n')
            elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
                self.file_manager.write(file_id, '    default         CrankNicolson 0.5;\n')
            elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
                self.file_manager.write(file_id, '    default         Euler;\n')
            elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
                self.file_manager.write(file_id, '    default         backward;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'gradSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            self.file_manager.write(file_id, '    default         cellLimited Gauss linear 0.33;\n')
            self.file_manager.write(file_id, '    grad(U)         cellLimited Gauss linear 0.33;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            self.file_manager.write(file_id, '    default         cellLimited Gauss linear 1;\n')
            self.file_manager.write(file_id, '    grad(U)         cellLimited Gauss linear 1;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            self.file_manager.write(file_id, '    default         cellLimited Gauss linear 1;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            self.file_manager.write(file_id, '    default         Gauss linear;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'divSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            if self.properties['numerical_discretisation']['use_first_order_for_turbulence']:
                self.file_manager.write(file_id, '    default         Gauss upwind ' + gradient_scheme + ';\n')
            else:
                self.file_manager.write(file_id, '    default         Gauss linearUpwind ' + gradient_scheme + ';\n')
            self.file_manager.write(file_id, '    div(phi,U)      Gauss linearUpwindV grad(U);\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            if self.properties['numerical_discretisation']['use_first_order_for_turbulence']:
                self.file_manager.write(file_id, '    default         bounded Gauss upwind ' + gradient_scheme + ';\n')
            else:
                self.file_manager.write(file_id, '    default         bounded Gauss Minmod ' + gradient_scheme + ';\n')
            self.file_manager.write(file_id, '    div(phi,U)      bounded Gauss MinmodV grad(U);\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            self.file_manager.write(file_id, '    default         bounded Gauss upwind;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            if self.properties['numerical_discretisation']['use_first_order_for_turbulence']:
                self.file_manager.write(file_id, '    default         Gauss upwind ' + gradient_scheme + ';\n')
            else:
                self.file_manager.write(file_id, '    default         Gauss limitedLinear 1;\n')
            self.file_manager.write(file_id, '    div(phi,U)      Gauss linear;\n')
        if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            self.file_manager.write(file_id, '    div((nuEff*dev2(T(grad(U))))) Gauss linear;\n')
        elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.file_manager.write(file_id, '    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'laplacianSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            self.file_manager.write(file_id, '    default         Gauss linear limited 0.33;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            self.file_manager.write(file_id, '    default         Gauss linear limited 1;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            self.file_manager.write(file_id, '    default         Gauss linear limited 1;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            self.file_manager.write(file_id, '    default         Gauss linear limited 0.33;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'interpolationSchemes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    default         linear;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'snGradSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            self.file_manager.write(file_id, '    default         limited 0.33;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            self.file_manager.write(file_id, '    default         limited 1;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            self.file_manager.write(file_id, '    default         limited 1;\n')
        elif self.properties['numerical_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            self.file_manager.write(file_id, '    default         limited 0.33;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

        self.file_manager.write(file_id, 'wallDist\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    method          meshWave;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
