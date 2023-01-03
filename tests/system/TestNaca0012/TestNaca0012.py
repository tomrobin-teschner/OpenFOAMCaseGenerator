from src.CaseGenerator.Properties.GlobalVariables import *
from ..TestCaseBase import TestCaseBase

class TestNaca0012(TestCaseBase):
    def setup_case(self):
        module = 'Naca0012'
        flow_type = FlowType.incompressible.name

        for rans_model in RansModel:
            # avoid qZeta model, will result in division by zero error
            # no documentation or test cases available by openfoam
            # to show how to correctly use this case
            if rans_model is not RansModel.qZeta:
                case_name = f'{module}_{flow_type}_{rans_model.name}'
                parameters = {'rans_model': rans_model, 'flow_type': flow_type}
                yield module, case_name, parameters
