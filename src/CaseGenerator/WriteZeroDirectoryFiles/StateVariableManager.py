from src.CaseGenerator.Properties import GlobalVariables as Parameters


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
        if self.properties['turbulence_properties']['turbulence_type'] == Parameters.RANS:
            self.__add_variable_based_on_rans_model()
        elif self.properties['turbulence_properties']['turbulence_type'] == Parameters.LES:
            self.__add_variable_based_on_les_model()

        # list storing all state variables that are not part of a turbulence model
        self.non_turbulence_state_variable = ['U', 'p', 'T']

    def get_active_variables(self):
        return self.variables

    def var_is_from_rans_turbulence_model(self, var):
        if var in self.non_turbulence_state_variable:
            return False
        else:
            return True

    def __add_variable_based_on_flow_type(self):
        if self.properties['flow_properties']['flow_type'] == Parameters.incompressible:
            self.variables['U'] = ['volVectorField', '[0 1 -1 0 0 0 0]']
            self.variables['p'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
        elif self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.variables['U'] = ['volVectorField', '[0 1 -1 0 0 0 0]']
            self.variables['p'] = ['volScalarField', '[1 -1 -2 0 0 0 0]']
            self.variables['T'] = ['volScalarField', '[0 0 0 1 0 0 0]']

    def __add_variable_based_on_rans_model(self):
        self.variables['nut'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.variables['alphat'] = ['volScalarField', '[1 -1 -1 0 0 0 0]']

        # turbulence model specific variables
        if self.properties['turbulence_properties']['turbulence_type'] == Parameters.RANS:
            rans_model = self.properties['turbulence_properties']['RANS_model']
            if (rans_model == Parameters.kEpsilon or rans_model == Parameters.realizableKE or
                    rans_model == Parameters.RNGkEpsilon or rans_model == Parameters.LienLeschziner or
                    rans_model == Parameters.LamBremhorstKE or rans_model == Parameters.LaunderSharmaKE or
                    rans_model == Parameters.qZeta or rans_model == Parameters.LienCubicKE or
                    rans_model == Parameters.ShihQuadraticKE):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['epsilon'] = ['volScalarField', '[0 2 -3 0 0 0 0]']
            elif rans_model == Parameters.kOmega or rans_model == Parameters.kOmegaSST:
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
            elif rans_model == Parameters.kOmegaSSTLM:
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
                self.variables['ReThetat'] = ['volScalarField', '[0 0 0 0 0 0 0]']
                self.variables['gammaInt'] = ['volScalarField', '[0 0 0 0 0 0 0]']
            elif rans_model == Parameters.kOmega or rans_model == Parameters.kOmegaSSTSAS:
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
            elif rans_model == Parameters.kkLOmega:
                self.variables['kt'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['kl'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
            elif rans_model == Parameters.SpalartAllmaras:
                self.variables['nuTilda'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
            elif rans_model == Parameters.LRR or rans_model == Parameters.SSG:
                self.variables['epsilon'] = ['volScalarField', '[0 2 -3 0 0 0 0]']
                self.variables['R'] = ['volSymmTensorField', '[0 2 -2 0 0 0 0]']

    def __add_variable_based_on_les_model(self):
        self.variables['nut'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
        if self.properties['flow_properties']['flow_type'] == Parameters.compressible:
            self.variables['alphat'] = ['volScalarField', '[1 -1 -1 0 0 0 0]']

        if self.properties['turbulence_properties']['turbulence_type'] == Parameters.LES:
            les_model = self.properties['turbulence_properties']['LES_model']
            if les_model == Parameters.kEqn or les_model == Parameters.dynamicKEqn:
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
            elif (les_model == Parameters.SpalartAllmarasDES or les_model == Parameters.SpalartAllmarasDDES or
                  les_model == Parameters.SpalartAllmarasIDDES):
                self.variables['nuTilda'] = ['volScalarField', '[0 2 -1 0 0 0 0]']
            elif (les_model == Parameters.kOmegaSSTDES or les_model == Parameters.kOmegaSSTDDES or
                  les_model == Parameters.kOmegaSSTIDDES):
                self.variables['k'] = ['volScalarField', '[0 2 -2 0 0 0 0]']
                self.variables['omega'] = ['volScalarField', '[0 0 -1 0 0 0 0]']
