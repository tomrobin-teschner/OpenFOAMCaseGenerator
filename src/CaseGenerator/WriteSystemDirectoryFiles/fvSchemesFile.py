from src.CaseGenerator.Properties.GlobalVariables import *
import src.CaseGenerator.WriteZeroDirectoryFiles as ZeroDir
from src.CaseGenerator.FileDirectoryIO import WriteHeader


class fvSchemesFile:
    def __init__(self, properties):
        self.properties = properties
        self.state_variable_manager = ZeroDir.StateVariableManager(properties)
        self.variable_names = self.state_variable_manager.get_active_variable_names()
        self.indentation = 42

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        fv_schemes = WriteHeader.get_header(version, 'dictionary', 'system', 'fvSchemes')

        fv_schemes += self.__get_ddt_schemes()
        fv_schemes += self.__get_grad_schemes()
        fv_schemes += self.__get_div_schemes()
        fv_schemes += self.__get_laplacian_schemes()
        fv_schemes += self.__get_interpolation_schemes()
        fv_schemes += self.__get_sn_grad_schemes()
        fv_schemes += self.__get_wall_dist_method()

        fv_schemes += f'\n// ************************************************************************* //\n'
        return fv_schemes

    def __get_ddt_schemes(self):
        temp = ''
        temp += f'ddtSchemes\n'
        temp += f'{{\n'
        if self.properties['time_discretisation']['time_integration'] == TimeTreatment.steady_state:
            temp += f'    default' + (self.indentation - 12) * ' ' + 'steadyState;\n'
        else:
            if self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.default:
                temp += f'    default' + (self.indentation - 12) * ' ' + 'CrankNicolson 0.5;\n'
            elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.tvd:
                temp += f'    default' + (self.indentation - 12) * ' ' + 'CrankNicolson 0.5;\n'
            elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.robustness:
                temp += f'    default' + (self.indentation - 12) * ' ' + 'Euler;\n'
            elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.accuracy:
                temp += f'    default' + (self.indentation - 12) * ' ' + 'backward;\n'
        temp += f'}}\n'
        temp += f'\n'
        return temp

    def __get_grad_schemes(self):
        temp = ''
        grad_type_U = ''
        grad_type_rest = ''
        if self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.default:
            grad_type_U += 'cellLimited Gauss linear 0.33;\n'
            grad_type_rest = 'Gauss linear;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.tvd:
            grad_type_U += 'cellLimited Gauss linear 1;\n'
            grad_type_rest = 'cellLimited Gauss linear 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.robustness:
            grad_type_U += 'cellLimited Gauss linear 1;\n'
            grad_type_rest = 'cellLimited Gauss linear 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.accuracy:
            grad_type_U += 'Gauss linear;\n'
            grad_type_rest = 'Gauss linear;\n'

        temp += f'gradSchemes\n'
        temp += f'{{\n'
        spacing = (self.indentation - 12) * ' '
        temp += f'    default{spacing}{grad_type_rest}'
        for var in self.variable_names:
            spacing = (self.indentation - len('    grad(' + var + ')') - 1) * ' '
            if var == 'U':
                temp += f'    grad({var}){spacing}{grad_type_U}'
            else:
                temp += f'    grad({var}){spacing}{grad_type_rest}'
        temp += f'}}\n'
        temp += f'\n'
        return temp

    def __get_div_schemes(self):
        temp = ''
        is_rans = self.properties['turbulence_properties']['RansModel']
        use_first_order = self.properties['spatial_discretisation']['use_first_order_for_turbulence']
        discretisation_policy = self.properties['spatial_discretisation']['numerical_schemes_correction']

        pre_default_test = ''
        if self.properties['turbulence_properties']['use_phi_instead_of_grad_U']:
            pre_default_test += 'phi '

        temp += f'divSchemes\n'
        temp += f'{{\n'

        spacing = (self.indentation - 12) * ' '
        if discretisation_policy == DiscretisationPolicy.default:
            div_type = 'Gauss linearUpwind ' + pre_default_test + 'default;\n'
        elif discretisation_policy == DiscretisationPolicy.tvd:
            div_type = 'Gauss Minmod ' + pre_default_test + 'default;\n'
        elif discretisation_policy == DiscretisationPolicy.robustness:
            div_type = 'Gauss upwind ' + pre_default_test + 'default;\n'
        elif discretisation_policy == DiscretisationPolicy.accuracy:
            div_type = 'Gauss limitedLinear ' + pre_default_test + '1;\n'
        temp += f'    default{spacing}{div_type}'

        # allow for explicit solvers as well (which may have a div(U) term instead of the linearised
        # div(phi, U) term only)
        div_type = 'Gauss linear;\n'
        spacing = (self.indentation - len('    div(U)') - 1) * ' '
        temp += f'    div(U){spacing}{div_type}'

        for var in self.variable_names:
            if discretisation_policy == DiscretisationPolicy.default:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                if var == 'U':
                    div_type = 'Gauss linearUpwindV grad(U);\n'
                elif not self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    div_type = 'Gauss linearUpwind grad(' + var + ');\n'
                elif self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    if is_rans and use_first_order:
                        div_type = 'Gauss upwind;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                    else:
                        div_type = 'Gauss linearUpwind grad(' + var + ');\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '

            elif discretisation_policy == DiscretisationPolicy.tvd:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                if var == 'U':
                    div_type = 'bounded Gauss MinmodV grad(U);\n'
                elif not self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    div_type = 'bounded Gauss Minmod grad(' + var + ');\n'
                elif self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    if is_rans and use_first_order:
                        div_type = 'bounded Gauss upwind;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                    else:
                        div_type = 'bounded Gauss Minmod;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '

            elif discretisation_policy == DiscretisationPolicy.robustness:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                div_type = 'bounded Gauss upwind;\n'

            elif discretisation_policy == DiscretisationPolicy.accuracy:
                spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                if var == 'U':
                    div_type = 'bounded Gauss MUSCLV grad(U);\n'
                elif not self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    div_type = 'Gauss limitedLinear 1;\n'
                elif self.state_variable_manager.var_is_from_rans_turbulence_model(var):
                    if is_rans and use_first_order:
                        div_type = 'Gauss upwind;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
                    else:
                        div_type = 'Gauss limitedLinear 1;\n'
                        spacing = (self.indentation - len('    div(phi,' + var + ')') - 1) * ' '
            temp += f'    div(phi,{var}){spacing}{div_type}'

        if self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
            spacing = (self.indentation - len('    div((nuEff*dev2(T(grad(U)))))') - 1) * ' '
            temp += f'    div((nuEff*dev2(T(grad(U))))){spacing}Gauss linear;\n'
        elif self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            spacing = (self.indentation - len('    div(((rho*nuEff)*dev2(T(grad(U)))))') - 1) * ' '
            temp += f'    div(((rho*nuEff)*dev2(T(grad(U))))){spacing}Gauss linear;\n'
        temp += f'}}\n'
        temp += f'\n'
        return temp

    def __get_laplacian_schemes(self):
        temp = ''
        laplacian_type = ''
        if self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.default:
            laplacian_type += 'Gauss linear limited 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.tvd:
            laplacian_type += 'Gauss linear limited 0;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.robustness:
            laplacian_type += 'Gauss linear limited 0.33;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.accuracy:
            laplacian_type += 'Gauss linear limited 1;\n'

        spacing = (self.indentation - 12) * ' '
        temp += f'laplacianSchemes\n'
        temp += f'{{\n'
        temp += f'    default{spacing}{laplacian_type}'

        # allow for explicit solvers as well (which may have a laplacian(p) term as well)
        spacing = (self.indentation - len('    laplacian(p)') - 1) * ' '
        temp += f'    laplacian(p){spacing}{laplacian_type}'

        for var in self.variable_names:
            spacing = (self.indentation - len('    laplacian(nuEff,' + var + ')') - 1) * ' '
            temp += f'    laplacian(nuEff,{var}){spacing}{laplacian_type}'
        temp += f'}}\n'
        temp += f'\n'
        return temp

    def __get_interpolation_schemes(self):
        temp = ''
        temp += f'interpolationSchemes\n'
        temp += f'{{\n'
        temp += f'    default' + (self.indentation - 12) * ' ' + 'linear;\n'
        for var in self.variable_names:
            spacing = (self.indentation - len('    flux(' + var + ')') - 1) * ' '
            temp += f'    flux({var}){spacing}linear;\n'
        temp += f'}}\n'
        temp += f'\n'
        return temp

    def __get_sn_grad_schemes(self):
        temp = ''
        surface_type = ''
        if self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.default:
            surface_type += 'limited 1;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.tvd:
            surface_type += 'limited 0;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.robustness:
            surface_type += 'limited 0.33;\n'
        elif self.properties['spatial_discretisation']['numerical_schemes_correction'] == DiscretisationPolicy.accuracy:
            surface_type += 'limited 1;\n'

        spacing = (self.indentation - 12) * ' '
        temp += f'snGradSchemes\n'
        temp += f'{{\n'
        temp += f'    default{spacing}{surface_type}'
        for var in self.variable_names:
            spacing = (self.indentation - len('    snGrad(' + var + ')') - 1) * ' '
            temp += f'    snGrad({var}){spacing}{surface_type}'
        temp += f'}}\n'
        temp += f'\n'
        return temp

    def __get_wall_dist_method(self):
        temp = ''
        temp += f'wallDist\n'
        temp += f'{{\n'
        temp += f'    method' + (self.indentation - 11) * ' ' + 'meshWave;\n'
        temp += f'}}\n'
        return temp
