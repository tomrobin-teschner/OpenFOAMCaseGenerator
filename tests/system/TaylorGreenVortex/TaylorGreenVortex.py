from src.CaseGenerator.Properties.GlobalVariables import *
from ..TestCaseBase import TestCaseBase

class TaylorGreenVortex(TestCaseBase):
    def setup_case(self):
        module = 'TaylorGreenVortex'
        flow_type = FlowType.compressible

        for les_model in LesModel:
            case_name = f'{module}_{flow_type.name}_{les_model.name}'
            parameters = {'les_model': les_model, 'flow_type': flow_type}
            yield module, case_name, parameters

        for delta_model in DeltaModel:
            case_name = f'{module}_{flow_type.name}_{les_model.name}'
            parameters = {'delta_model': delta_model, 'flow_type': flow_type}
            yield module, case_name, parameters

        for filter in LesFilter:
            case_name = f'{module}_{flow_type.name}_{les_model.name}'
            parameters = {'les_model': LesModel.dynamicLagrangian, 'les_filter': filter, 'flow_type': flow_type}
            yield module, case_name, parameters
