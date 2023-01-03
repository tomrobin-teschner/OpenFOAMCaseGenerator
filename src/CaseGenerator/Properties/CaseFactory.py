import importlib
import sys


class CaseFactory:
    def __init__(self, case_name, parameters):
        self.case_name = case_name
        self.parameters = parameters

    def get_case_properties(self):
        try:
            case = getattr(importlib.import_module(f'input.cases.{self.case_name}.{self.case_name}'), self.case_name)
        except:
            sys.exit(
                f'Could not process the input: input/cases/{self.case_name}/{self.case_name}.py\n' +
                f'Please ensure the file exists in the input directory and is spelled correctly. If it does\n' +
                f'exist, ensure that the class name within {self.case_name}.py contains a class of the\n'
                f'same name and derives from the base class, e.g.:\n\nclass {self.case_name}'
                f'(BaseCase):\n\nThe program will terminate now.'
            )

        test_case = case()
        if self.parameters is not {}:
            test_case.parameters.update(self.parameters)
        test_case.create_case()
        return test_case.get_properties()
