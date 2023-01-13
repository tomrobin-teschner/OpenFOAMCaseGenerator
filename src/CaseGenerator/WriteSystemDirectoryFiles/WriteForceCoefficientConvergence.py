from src.CaseGenerator.Properties.GlobalVariables import *


class WriteForceCoefficientConvergence:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_triggers(self):
        wait_n_time_steps = self.properties['convergence_control']['time_steps_to_wait_before_checking_convergence']
        convergence = str(self.properties['convergence_control']['integral_quantities_convergence_threshold'])
        averaging_time = str(self.properties['convergence_control']['averaging_time_steps'])
        quantities_to_observe = self.properties['convergence_control']['integral_convergence_criterion']
        count = 1

        file_id = self.file_manager.create_file('system/include', 'forceCoefficientTrigger')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'forceCoefficientConvergenceTrigger')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'runTimeControl1\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            runTimeControl;\n')
        self.file_manager.write(file_id, '    libs            (utilityFunctionObjects);\n')
        self.file_manager.write(file_id, '    controlMode     trigger;\n')
        self.file_manager.write(file_id, '    triggerStart    1;\n')
        self.file_manager.write(file_id, '    conditions\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        condition1\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            type            average;\n')
        self.file_manager.write(file_id, '            functionObject  forceCoeffs;\n')
        self.file_manager.write(file_id, '            fields          (')
        for quantity in quantities_to_observe:
            self.file_manager.write(file_id, self.__quantity_ID_to_string(quantity))
            if count != len(quantities_to_observe):
                self.file_manager.write(file_id, ' ')
            count += 1
        self.file_manager.write(file_id, ');\n')
        self.file_manager.write(file_id, '            tolerance       ' + convergence + ';\n')
        self.file_manager.write(file_id, '            window          ' + averaging_time + ';\n')
        self.file_manager.write(file_id, '            windowType      approximate;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'runTimeControl2\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            runTimeControl;\n')
        self.file_manager.write(file_id, '    libs            (utilityFunctionObjects);\n')
        self.file_manager.write(file_id, '    conditions\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        conditions1\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            type            maxDuration;\n')
        if self.properties['time_discretisation']['time_integration'] == TimeTreatment.steady_state:
            self.file_manager.write(file_id, '            duration        ' + str(wait_n_time_steps) + ';\n')
        elif self.properties['time_discretisation']['time_integration'] == TimeTreatment.unsteady:
            wait_until = self.properties['time_discretisation']['unsteady_properties']['deltaT'] * wait_n_time_steps
            self.file_manager.write(file_id, '            duration        ' + str(wait_until) + ';\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '    satisfiedAction setTrigger;\n')
        self.file_manager.write(file_id, '    trigger         1;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')

    def __quantity_ID_to_string(self, quantity):
        if quantity == IntegralQuantities.c_l:
            return 'Cl'
        if quantity == IntegralQuantities.c_d:
            return 'Cd'
        if quantity == IntegralQuantities.c_s:
            return 'Cs'
        if quantity == IntegralQuantities.c_m_yaw:
            return 'CmYaw'
        if quantity == IntegralQuantities.c_m_roll:
            return 'CmRoll'
        if quantity == IntegralQuantities.c_m_pitch:
            return 'CmPitch'
