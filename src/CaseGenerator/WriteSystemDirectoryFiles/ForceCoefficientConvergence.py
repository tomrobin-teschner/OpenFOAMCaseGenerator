from src.CaseGenerator.FileDirectoryIO import WriteHeader
from src.CaseGenerator.Properties.GlobalVariables import *

class ForceCoefficientConvergence:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        wait_n_time_steps = self.properties['convergence_control']['time_steps_to_wait_before_checking_convergence']
        convergence = str(self.properties['convergence_control']['integral_quantities_convergence_threshold'])
        averaging_time = str(self.properties['convergence_control']['averaging_time_steps'])
        quantities_to_observe = self.properties['convergence_control']['integral_convergence_criterion']
        count = 1
        
        version = self.properties['file_properties']['version']
        triggers = WriteHeader.get_header(version, 'dictionary', 'system', 'forceCoefficientConvergenceTrigger')

        triggers += f'\n'
        triggers += f'runTimeControl1\n'
        triggers += f'{{\n'
        triggers += f'    type            runTimeControl;\n'
        triggers += f'    libs            (utilityFunctionObjects);\n'
        triggers += f'    controlMode     trigger;\n'
        triggers += f'    triggerStart    1;\n'
        triggers += f'    conditions\n'
        triggers += f'    {{\n'
        triggers += f'        condition1\n'
        triggers += f'        {{\n'
        triggers += f'            type            average;\n'
        triggers += f'            functionObject  forceCoeffs;\n'
        triggers += f'            fields          ('
        for quantity in quantities_to_observe:
            triggers += f'{quantity.name}'
            if count != len(quantities_to_observe):
                triggers += f' '
            count += 1
        triggers += f');\n'
        triggers += f'            tolerance       {convergence};\n'
        triggers += f'            window          {averaging_time};\n'
        triggers += f'            windowType      approximate;\n'
        triggers += f'        }}\n'
        triggers += f'    }}\n'
        triggers += f'}}\n'
        triggers += f'\n'
        triggers += f'runTimeControl2\n'
        triggers += f'{{\n'
        triggers += f'    type            runTimeControl;\n'
        triggers += f'    libs            (utilityFunctionObjects);\n'
        triggers += f'    conditions\n'
        triggers += f'    {{\n'
        triggers += f'        conditions1\n'
        triggers += f'        {{\n'
        triggers += f'            type            maxDuration;\n'
        if self.properties['time_discretisation']['time_integration'] == TimeTreatment.steady_state:
            triggers += f'            duration        {wait_n_time_steps};\n'
        elif self.properties['time_discretisation']['time_integration'] == TimeTreatment.unsteady:
            wait_until = self.properties['time_discretisation']['unsteady_properties']['deltaT'] * wait_n_time_steps
            triggers += f'            duration        {wait_until};\n'
        triggers += f'        }}\n'
        triggers += f'    }}\n'
        triggers += f'    satisfiedAction setTrigger;\n'
        triggers += f'    trigger         1;\n'
        triggers += f'}}\n'
        triggers += f'// ************************************************************************* //\n'
        return triggers
