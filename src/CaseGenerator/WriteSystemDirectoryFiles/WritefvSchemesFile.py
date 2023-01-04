from src.CaseGenerator.Properties import GlobalVariables as Parameters
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir


class fvSchemesFile:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager
        self.state_variable_manager = ZeroDir.StateVariableManager(properties)
        self.variable_names = self.state_variable_manager.get_active_variable_names()
        self.indentation = 38

    def write_input_file(self):
        file_id = self.file_manager.create_file('system', 'fvSchemes')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fvSchemes')
        self.file_manager.write(file_id, '\n')

        self.__write_ddt_schemes(file_id)
        self.__write_grad_schemes(file_id)
        self.__write_div_schemes(file_id)
        self.__write_laplacian_schemes(file_id)
        self.__write_interpolation_schemes(file_id)
        self.__write_sn_grad_schemes(file_id)
        self.__write_wall_dist_method(file_id)

        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)

    def __write_ddt_schemes(self, file_id):
        self.file_manager.write(file_id, 'ddtSchemes\n')
        self.file_manager.write(file_id, '{\n')
        if self.properties['time_discretisation']['time_integration'] == Parameters.STEADY_STATE:
            self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + 'steadyState;\n')
        else:
            if self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
                self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + 'CrankNicolson 0.5;\n')
            elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
                self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + 'CrankNicolson 0.5;\n')
            elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
                self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + 'Euler;\n')
            elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
                self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + 'backward;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

    def __write_grad_schemes(self, file_id):
        grad_type_U = ''
        grad_type_rest = ''
        if self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            grad_type_U += 'cellLimited Gauss linear 0.33;\n'
            grad_type_rest = 'Gauss linear;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            grad_type_U += 'cellLimited Gauss linear 1;\n'
            grad_type_rest = 'cellLimited Gauss linear 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            grad_type_U += 'cellLimited Gauss linear 1;\n'
            grad_type_rest = 'cellLimited Gauss linear 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            grad_type_U += 'Gauss linear;\n'
            grad_type_rest = 'Gauss linear;\n'

        self.file_manager.write(file_id, 'gradSchemes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + grad_type_rest)
        for var in self.variable_names:
            spacing = (self.indentation - len('    grad(' + var + ')') - 1) * ' '
            if var == 'U':
                self.file_manager.write(file_id, '    grad(' + var + ')' + spacing + grad_type_U)
            else:
                self.file_manager.write(file_id, '    grad(' + var + ')' + spacing + grad_type_rest)
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

    def __write_div_schemes(self, file_id):
        is_rans = self.properties['turbulence_properties']['RANS_model']
        use_first_order = self.properties['spatial_discretisation']['use_first_order_for_turbulence']
        discretisation_policy = self.properties['spatial_discretisation']['numerical_schemes_correction']

        pre_default_test = ''
        if self.properties['turbulence_properties']['use_phi_instead_of_grad_U']:
            pre_default_test += 'phi '

        self.file_manager.write(file_id, 'divSchemes\n')
        self.file_manager.write(file_id, '{\n')

        if discretisation_policy == Parameters.DEFAULT:
            div_type = 'Gauss linearUpwind ' + pre_default_test + 'default;\n'
            self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + div_type)
        elif discretisation_policy == Parameters.TVD:
            div_type = 'Gauss Minmod ' + pre_default_test + 'default;\n'
            self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + div_type)
        elif discretisation_policy == Parameters.ROBUSTNESS:
            div_type = 'Gauss upwind ' + pre_default_test + 'default;\n'
            self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + div_type)
        elif discretisation_policy == Parameters.ACCURACY:
            div_type = 'Gauss limitedLinear ' + pre_default_test + '1;\n'
            self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + div_type)

        # allow for explicit solvers as well (which may have a div(U) term instead of the linearised
        # div(phi, U) term only)
        div_type = 'Gauss linear;\n'
        spacing = (self.indentation - len('    div(U)') - 1) * ' '
        self.file_manager.write(file_id, '    div(U)' + spacing + div_type)

        for var in self.variable_names:
            if discretisation_policy == Parameters.DEFAULT:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                if var == 'U':
                    div_type = 'Gauss linearUpwindV grad(U);\n'
                    self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                elif not self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    div_type = 'Gauss linearUpwind grad(' + var + ');\n'
                    self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                elif self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    if is_rans and use_first_order:
                        div_type = 'Gauss upwind;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                        self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                    else:
                        div_type = 'Gauss linearUpwind grad(' + var + ');\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                        self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)

            elif discretisation_policy == Parameters.TVD:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                if var == 'U':
                    div_type = 'bounded Gauss MinmodV grad(U);\n'
                    self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                elif not self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    div_type = 'bounded Gauss Minmod grad(' + var + ');\n'
                    self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                elif self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    if is_rans and use_first_order:
                        div_type = 'bounded Gauss upwind;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                        self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                    else:
                        div_type = 'bounded Gauss Minmod;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                        self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)

            elif discretisation_policy == Parameters.ROBUSTNESS:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                div_type = 'bounded Gauss upwind;\n'
                self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)

            elif discretisation_policy == Parameters.ACCURACY:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                if var == 'U':
                    div_type = 'bounded Gauss MUSCLV grad(U);\n'
                    self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                elif not self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    div_type = 'Gauss limitedLinear 1;\n'
                    self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                elif self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    if is_rans and use_first_order:
                        div_type = 'Gauss upwind;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                        self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)
                    else:
                        div_type = 'Gauss limitedLinear 1;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                        self.file_manager.write(file_id, '    div(phi,' + var + ')' + spacing + div_type)

        if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            spacing = (self.indentation - len('    div((nuEff*dev2(T(grad(U)))))') - 1) * ' '
            self.file_manager.write(file_id, '    div((nuEff*dev2(T(grad(U)))))' + spacing + 'Gauss linear;\n')
        elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            spacing = (self.indentation - len('    div(((rho*nuEff)*dev2(T(grad(U)))))') - 1) * ' '
            self.file_manager.write(file_id, '    div(((rho*nuEff)*dev2(T(grad(U)))))' + spacing + 'Gauss linear;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

    def __write_laplacian_schemes(self, file_id):
        laplacian_type = ''
        if self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            laplacian_type += 'Gauss linear limited 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            laplacian_type += 'Gauss linear limited 0;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            laplacian_type += 'Gauss linear limited 0.33;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            laplacian_type += 'Gauss linear limited 1;\n'

        self.file_manager.write(file_id, 'laplacianSchemes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + laplacian_type)

        # allow for explicit solvers as well (which may have a laplacian(p) term as well)
        spacing = (self.indentation - len('    laplacian(p)') - 1) * ' '
        self.file_manager.write(file_id, '    laplacian(p)' + spacing + laplacian_type)

        for var in self.variable_names:
            spacing = (self.indentation - len('    laplacian(nuEff,' + var + ')') - 1) * ' '
            self.file_manager.write(file_id, '    laplacian(nuEff,' + var + ')' + spacing + laplacian_type)
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

    def __write_interpolation_schemes(self, file_id):
        self.file_manager.write(file_id, 'interpolationSchemes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + 'linear;\n')
        for var in self.variable_names:
            spacing = (self.indentation - len('    flux(' + var + ')') - 1) * ' '
            self.file_manager.write(file_id, '    flux(' + var + ')' + spacing + 'linear;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

    def __write_sn_grad_schemes(self, file_id):
        surface_type = ''
        if self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.DEFAULT:
            surface_type += 'limited 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.TVD:
            surface_type += 'limited 0;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ROBUSTNESS:
            surface_type += 'limited 0.33;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == Parameters.ACCURACY:
            surface_type += 'limited 1;\n'

        self.file_manager.write(file_id, 'snGradSchemes\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    default' + (self.indentation - 12) * ' ' + surface_type)
        for var in self.variable_names:
            spacing = (self.indentation - len('    snGrad(' + var + ')') - 1) * ' '
            self.file_manager.write(file_id, '    snGrad(' + var + ')' + spacing + surface_type)
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')

    def __write_wall_dist_method(self, file_id):
        self.file_manager.write(file_id, 'wallDist\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    method' + (self.indentation - 11) * ' ' + 'meshWave;\n')
        self.file_manager.write(file_id, '}\n')
