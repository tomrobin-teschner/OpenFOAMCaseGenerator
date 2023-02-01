from src.CaseGenerator.FileDirectoryIO.WriteHeader import WriteHeader
from src.CaseGenerator.Properties.GlobalVariables import *

class ThermophysicalProperties:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        is_const_viscosity = self.properties['flow_properties']['const_viscosity']
        material = self.properties['flow_properties']['dimensional_properties']['material_properties']
        
        eos = self.properties['flow_properties']['equation_of_state']
        energy_equation = self.properties['flow_properties']['energy_equation']
        thermo = f'hConst'
        thermoType = f'hePsiThermo'

        if is_const_viscosity:
            transport = f'const'
            transport_content = (
                f'        mu          {material["mu"]};\n'
                f'        Pr          {material["Pr"]};\n'
            )
        else:
            transport = f'sutherland'
            transport_content = (
                f'        As          {material["As"]};\n'
                f'        Ts          {material["Ts"]};\n'
            )

        header = WriteHeader.get_header(version, 'dictionary', 'constant', 'thermophysicalProperties')
        
        return (
            f'{header}'
            f'thermoType\n'
            f'{{\n'
            f'    type            {thermoType};\n'
            f'    mixture         pureMixture;\n'
            f'    transport       {transport};\n'
            f'    thermo          {thermo};\n'
            f'    equationOfState {eos.name};\n'
            f'    specie          specie;\n'
            f'    energy          {energy_equation.name};\n'
            f'}}\n'
            f'\n'
            f'mixture\n'
            f'{{\n'
            f'    specie\n'
            f'    {{\n'
            f'        molWeight   {material["molWeight"]};\n'
            f'    }}\n'
            f'    thermodynamics\n'
            f'    {{\n'
            f'        Cp          {material["Cp"]};\n'
            f'        Hf          {material["Hf"]};\n'
            f'    }}\n'
            f'    transport\n'
            f'    {{\n'
            f'{transport_content}'
            f'    }}\n'
            f'}}\n'
            f'\n'
            f'// ************************************************************************* //\n'
        )
