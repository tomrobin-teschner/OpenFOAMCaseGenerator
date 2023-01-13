from src.CaseGenerator.Properties.GlobalVariables import *
from src.CaseGenerator.FileDirectoryIO.WriteHeader import WriteHeader


class TurbulencePropertiesFile:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        turbulence_type = self.properties['turbulence_properties']['turbulence_type']

        if turbulence_type == TurbulenceType.laminar:
            simulation_type = f'simulationType laminar;\n'
            turbulence_setup = ''
        if turbulence_type == TurbulenceType.rans:
            simulation_type = f'simulationType RAS;\n'
            turbulence_setup = self.__get_RANS()
        if turbulence_type == TurbulenceType.les:
            simulation_type = f'simulationType LES;\n'
            turbulence_setup = self.__get_LES()
        header = WriteHeader.get_header(version, 'dictionary', 'constant', 'turbulenceProperties')

        return (
            f'{header}'
            f'{simulation_type}'
            f'\n'
            f'{turbulence_setup}'
            f'\n'
            f'// ************************************************************************* //\n'
        )
    
    def __get_RANS(self):
        rans_model = self.properties['turbulence_properties']['RansModel']
        rans_string = f'    RASModel        {rans_model.name};\n'       
        delta_model = ''
        if rans_model == RansModel.kOmegaSSTSAS:
            delta_model = self.__get_DeltaModel()
        
        return (
            f'RAS\n{{\n'
            f'{rans_string}'
            f'\n'
            f'    turbulence      on;\n'
            f'\n'
            f'    printCoeffs     on;\n'
            f'{delta_model}'
            f'}}\n'
        )

    def __get_LES(self):
        les_model = self.properties['turbulence_properties']['LesModel']
        les_model_string = f'    LESModel        {les_model.name};\n'
        
        filter_string = ''
        if les_model is LesModel.dynamicKEqn:
            filter_string = self.__get_filter_model()
        
        delta_string = self.__get_DeltaModel()

        return (
            f'LES\n{{\n'
            f'{les_model_string}'
            f'\n'
            f'    turbulence      on;\n'
            f'\n'
            f'    printCoeffs     on;\n'
            f'\n'
            f'{filter_string}'
            f'{delta_string}'
            f'}}\n\n'
        )

    def __get_filter_model(self):
        les_filter = self.properties['turbulence_properties']['LesFilter']
        return f'    filter          {les_filter.name};\n\n'

    def __get_DeltaModel(self):
        # if IDDES is used, delta model must be IDDES, silently overwrite it here in case wrong model is set
        les_model = self.properties['turbulence_properties']['LesModel']
        if (
                les_model == LesModel.SpalartAllmarasIDDES or
                les_model is LesModel.kOmegaSSTIDDES
            ):
            self.properties['turbulence_properties']['DeltaModel'] = DeltaModel.IDDESDelta

        delta_model = self.properties['turbulence_properties']['DeltaModel']
        delta_string = f'    delta           {delta_model.name};\n'
        
        return (
            f'{delta_string}\n'
            f'    cubeRootVolCoeffs\n'
            f'    {{\n'
            f'        deltaCoeff        1;\n'
            f'    }}\n'
            f'\n'
            f'    PrandtlCoeffs\n'
            f'    {{\n'
            f'        delta           cubeRootVol;\n'
            f'        cubeRootVolCoeffs\n'
            f'        {{\n'
            f'            deltaCoeff      1;\n'
            f'        }}\n'
            f'\n'
            f'        smoothCoeffs\n'
            f'        {{\n'
            f'            delta           cubeRootVol;\n'
            f'            cubeRootVolCoeffs\n'
            f'            {{\n'
            f'                deltaCoeff      1;\n'
            f'            }}\n'
            f'\n'
            f'            maxDeltaRatio   1.1;\n'
            f'        }}\n'
            f'\n'
            f'        Cdelta          0.158;\n'
            f'    }}\n'
            f'\n'
            f'    vanDriestCoeffs\n'
            f'    {{\n'
            f'        delta           cubeRootVol;\n'
            f'        cubeRootVolCoeffs\n'
            f'        {{\n'
            f'            deltaCoeff      1;\n'
            f'        }}\n'
            f'\n'
            f'        smoothCoeffs\n'
            f'        {{\n'
            f'            delta           cubeRootVol;\n'
            f'            cubeRootVolCoeffs\n'
            f'            {{\n'
            f'                deltaCoeff      1;\n'
            f'            }}\n'
            f'\n'
            f'            maxDeltaRatio   1.1;\n'
            f'        }}\n'
            f'\n'
            f'        Aplus           26;\n'
            f'        Cdelta          0.158;\n'
            f'    }}\n'
            f'\n'
            f'    smoothCoeffs\n'
            f'    {{\n'
            f'        delta           cubeRootVol;\n'
            f'        cubeRootVolCoeffs\n'
            f'        {{\n'
            f'            deltaCoeff      1;\n'
            f'        }}\n'
            f'\n'
            f'        maxDeltaRatio   1.1;\n'
            f'    }}\n'
        )
