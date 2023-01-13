from src.CaseGenerator.Properties.GlobalVariables import *


class StateVariableManager:
    def __init__(self, properties):
        self.properties = properties

        # list of all variables managed by this class. Each variable is mapped to a list of properties that contains
        # the following information
        #
        #   first index:    type of boundary field (either of scalar, vector or tensor type)
        #   second index:   dimension of of boundary field
        #
        # As a minimum, we need at least velocity and pressure but this list will increase based on other variables
        # that need to be solved for, i.e. for turbulent calculations, which is managed below.
        self.variables = {}
        self.__add_variable_based_on_flow_type()
        if self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.rans:
            self.__add_variable_based_on_RansModel()
        elif self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.les:
            self.__add_variable_based_on_LesModel()

        # list storing all state variables that are not part of a turbulence model
        self.non_turbulence_state_variable = ['U', 'p', 'T']

    def get_active_variable_names(self):
        names = []
        for key, value in self.variables.items():
            names.append(key)
        return names

    def get_active_variable_field_types(self):
        field_types = []
        for key, value in self.variables.items():
            field_types.append(value[0])
        return field_types

    def get_active_variable_dimensions(self):
        dimensions = []
        for key, value in self.variables.items():
            dimensions.append(value[1])
        return dimensions

    def var_is_from_rans_turbulence_model(self, var):
        if var in self.non_turbulence_state_variable:
            return False
        else:
            return True

    def __add_variable_based_on_flow_type(self):
        if self.properties['flow_properties']['flow_type'] == FlowType.incompressible:
            self.variables['U'] = ['volVectorField', '[0 1 -1 0 0 0 0]']
            self.variables['p'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
        elif self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            self.variables['U'] = ['volVectorField', '[0 1 -1 0 0 0 0]']
            self.variables['p'] = ['volScalarField', '[1 -1 -2 0 0 0 0]']
            self.variables['T'] = ['volScalarField', '[0 0 0 1 0 0 0]']

    def __add_variable_based_on_RansModel(self):
        self.variables['nut'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
        if self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            self.variables['alphat'] = ['volScalarField', '[1 -1 -1 0 0 0 0]']

        # turbulence model specific variables
        if self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.rans:
            RansModel = self.properties['turbulence_properties']['RansModel']
            if (
                    RansModel == RansModel.kEpsilon or
                    RansModel == RansModel.realizableKE or
                    RansModel == RansModel.RNGkEpsilon or
                    RansModel == RansModel.LienLeschziner or
                    RansModel == RansModel.LamBremhorstKE or
                    RansModel == RansModel.LaunderSharmaKE or
                    RansModel == RansModel.qZeta or
                    RansModel == RansModel.LienCubicKE or
                    RansModel == RansModel.ShihQuadraticKE
                ):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['epsilon'] = ['volScalarField', '[0 2 -3 0 0 0 0]']
            elif (
                    RansModel == RansModel.kOmega or
                    RansModel == RansModel.kOmegaSST
                ):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
            elif RansModel == RansModel.kOmegaSSTLM:
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
                self.variables['ReThetat'] = ['volScalarField', '[0 0 0 0 0 0 0]']
                self.variables['gammaInt'] = ['volScalarField', '[0 0 0 0 0 0 0]']
            elif (
                    RansModel == RansModel.kOmega or
                    RansModel == RansModel.kOmegaSSTSAS
                ):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
            elif RansModel == RansModel.kkLOmega:
                self.variables['kt'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['kl'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
            elif RansModel == RansModel.SpalartAllmaras:
                self.variables['nuTilda'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
            elif (
                    RansModel == RansModel.LRR or
                    RansModel == RansModel.SSG
                ):
                self.variables['epsilon'] = ['volScalarField', '[0 2 -3 0 0 0 0]']
                self.variables['R'] = ['volSymmTensorField', '[0 2 -2 0 0 0 0]']

    def __add_variable_based_on_LesModel(self):
        self.variables['nut'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
        if self.properties['flow_properties']['flow_type'] == FlowType.compressible:
            self.variables['alphat'] = ['volScalarField', '[1 -1 -1 0 0 0 0]']

        if self.properties['turbulence_properties']['turbulence_type'] == TurbulenceType.les:
            LesModel = self.properties['turbulence_properties']['LesModel']
            if (
                    LesModel == LesModel.kEqn or
                    LesModel == LesModel.dynamicKEqn
                ):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
            elif (
                    LesModel == LesModel.SpalartAllmarasDES or
                    LesModel == LesModel.SpalartAllmarasDDES or
                    LesModel == LesModel.SpalartAllmarasIDDES
                ):
                self.variables['nuTilda'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
            elif (
                    LesModel == LesModel.kOmegaSSTDES or
                    LesModel == LesModel.kOmegaSSTDDES or
                    LesModel == LesModel.kOmegaSSTIDDES
                ):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
