import src.CaseGenerator.Properties.CaseProperties as CaseProperties
import src.CaseGenerator.FileDirectoryIO as FileIO
import src.CaseGenerator.Checker as Checker
from src.CaseGenerator.Properties.CaseFactory import CaseFactory
from src.CaseGenerator.Properties.CaseProperties import CaseProperties
from src.CaseGenerator import CaseGenerator


def main():
    # process command line arguments first
    command_line_arguments = Checker.CheckCommandLineArguments()

    # create case
    case_name  = command_line_arguments['case']
    parameters = command_line_arguments['parameter']
    factory = CaseFactory(case_name, parameters)

    # add additional, default parameters to properties
    case_handler    = CaseProperties()
    case_properties = factory.get_case_properties()
    case_properties = case_handler.add_default_properties(case_properties)

    # hand-off case generation to dedicated class
    case = CaseGenerator(case_properties)
    case.generate_case()

    # output diagnostics
    screen_output = FileIO.ScreenOutput(case_properties)
    screen_output.print_summary(command_line_arguments)


if __name__ == '__main__':
    main()
