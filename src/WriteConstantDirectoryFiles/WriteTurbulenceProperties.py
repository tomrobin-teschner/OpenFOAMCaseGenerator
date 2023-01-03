from src.Properties import GlobalVariables as Parameters


class TurbulencePropertiesFile:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        turbulence_type = self.properties['turbulence_properties']['turbulence_type']

        if turbulence_type == Parameters.LAMINAR:
            simulation_type = f'simulationType laminar;\n'
            turbulence_setup = ''
        if turbulence_type == Parameters.RANS:
            simulation_type = f'simulationType RAS;\n'
            turbulence_setup = self.__get_RANS()
        if turbulence_type == Parameters.LES:
            simulation_type = f'simulationType LES;\n'
            turbulence_setup = self.__get_LES()

        return (
            f'/*--------------------------------*- C++ -*----------------------------------*\\\n'
            f'| =========                 |                                                 |\n'
            f'| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n'
            f'|  \\\    /   O peration     | Version:  {version}                                 |\n'
            f'|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |\n'
            f'|    \\\/     M anipulation  |                                                 |\n'
            f'\*---------------------------------------------------------------------------*/\n'
            f'FoamFile\n'
            f'{{\n'
            f'    version     2.0;\n'
            f'    format      ascii;\n'
            f'    class       dictionary;\n'
            f'    location    "constant";\n'
            f'    object      turbulenceProperties;\n'
            f'}}\n'
            f'// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'
            f'\n'
            f'{simulation_type}'
            f'\n'
            f'{turbulence_setup}'
            f'\n'
            f'// ************************************************************************* //\n'
        )
    
    def __get_RANS(self):
        rans_model = self.properties['turbulence_properties']['RANS_model']
        if rans_model == Parameters.kEpsilon:
            rans_string = f'    RASModel        kEpsilon;\n'
        elif rans_model == Parameters.realizableKE:
            rans_string = f'    RASModel        realizableKE;\n'
        elif rans_model == Parameters.RNGkEpsilon:
            rans_string = f'    RASModel        RNGkEpsilon;\n'
        elif rans_model == Parameters.LienLeschziner:
            rans_string = f'    RASModel        LienLeschziner;\n'
        elif rans_model == Parameters.LamBremhorstKE:
            rans_string = f'    RASModel        LamBremhorstKE;\n'
        elif rans_model == Parameters.LaunderSharmaKE:
            rans_string = f'    RASModel        LaunderSharmaKE;\n'
        elif rans_model == Parameters.kOmega:
            rans_string = f'    RASModel        kOmega;\n'
        elif rans_model == Parameters.kOmegaSST:
            rans_string = f'    RASModel        kOmegaSST;\n'
        elif rans_model == Parameters.kOmegaSSTLM:
            rans_string = f'    RASModel        kOmegaSSTLM;\n'
        elif rans_model == Parameters.kkLOmega:
            rans_string = f'    RASModel        kkLOmega;\n'
        elif rans_model == Parameters.kOmegaSSTSAS:
            rans_string = f'    RASModel        kOmegaSSTSAS;\n'
        elif rans_model == Parameters.qZeta:
            rans_string = f'    RASModel        qZeta;\n'
        elif rans_model == Parameters.SpalartAllmaras:
            rans_string = f'    RASModel        SpalartAllmaras;\n'
        elif rans_model == Parameters.LienCubicKE:
            rans_string = f'    RASModel        LienCubicKE;\n'
        elif rans_model == Parameters.ShihQuadraticKE:
            rans_string = f'    RASModel        ShihQuadraticKE;\n'
        elif rans_model == Parameters.LRR:
            rans_string = f'    RASModel        LRR;\n'
        elif rans_model == Parameters.SSG:
            rans_string = f'    RASModel        SSG;\n'
        
        delta_model = ''
        if rans_model == Parameters.kOmegaSSTSAS:
            delta_model = self.__get_delta_model()
        
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
        les_model = self.properties['turbulence_properties']['LES_model']

        if les_model == Parameters.Smagorinsky:
            les_model_string = f'    LESModel        Smagorinsky;\n'
        elif les_model == Parameters.kEqn:
            les_model_string = f'    LESModel        kEqn;\n'
        elif les_model == Parameters.dynamicKEqn:
            les_model_string = f'    LESModel        dynamicKEqn;\n'
        elif les_model == Parameters.dynamicLagrangian:
            les_model_string = f'    LESModel        dynamicLagrangian;\n'
        elif les_model == Parameters.DeardorffDiffStress:
            les_model_string = f'    LESModel        DeardorffDiffStress;\n'
        elif les_model == Parameters.WALE:
            les_model_string = f'    LESModel        WALE;\n'
        elif les_model == Parameters.SpalartAllmarasDES:
            les_model_string = f'    LESModel        SpalartAllmarasDES;\n'
        elif les_model == Parameters.SpalartAllmarasDDES:
            les_model_string = f'    LESModel        SpalartAllmarasDDES;\n'
        elif les_model == Parameters.SpalartAllmarasIDDES:
            les_model_string = f'    LESModel        SpalartAllmarasIDDES;\n'
        elif les_model == Parameters.kOmegaSSTDES:
            les_model_string = f'    LESModel        kOmegaSSTDES;\n'
        elif les_model == Parameters.kOmegaSSTDDES:
            les_model_string = f'    LESModel        kOmegaSSTDDES;\n'
        elif les_model == Parameters.kOmegaSSTIDDES:
            les_model_string = f'    LESModel        kOmegaSSTIDDES;\n'
        
        filter_string = ''
        if les_model is Parameters.dynamicKEqn:
            filter_string = self.__get_filter_model()
        
        delta_string = self.__get_delta_model()


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
        les_filter = self.properties['turbulence_properties']['LES_filter']
        if les_filter is Parameters.SIMPLE_FILTER:
            return '    filter          simple;\n\n'
        elif les_filter is Parameters.ANISOTROPIC_FILTER:
            return '    filter          anisotropic;\n\n'
        elif les_filter is Parameters.LAPLACE_FILTER:
            return '    filter          laplace;\n\n'

    def __get_delta_model(self):
        # if IDDES is used, delta model must be IDDES, silently overwrite it here in case wrong model is set
        les_model = self.properties['turbulence_properties']['LES_model']
        if les_model == Parameters.SpalartAllmarasIDDES or les_model is Parameters.kOmegaSSTIDDES:
            self.properties['turbulence_properties']['delta_model'] = Parameters.IDDESDelta

        delta_model = self.properties['turbulence_properties']['delta_model']

        if delta_model == Parameters.smooth:
            delta_string = f'    delta           smooth;\n'
        elif delta_model == Parameters.Prandtl:
            delta_string = f'    delta           Prandtl;\n'
        elif delta_model == Parameters.maxDeltaxyz:
            delta_string = f'    delta           maxDeltaxyz;\n'
        elif delta_model == Parameters.cubeRootVol:
            delta_string = f'    delta           cubeRootVol;\n'
        elif delta_model == Parameters.maxDeltaxyzCubeRoot:
            delta_string = f'    delta           maxDeltaxyzCubeRoot;\n'
        elif delta_model == Parameters.vanDriest:
            delta_string = f'    delta           vanDriest;\n'
        elif delta_model == Parameters.IDDESDelta:
            delta_string = f'    delta           IDDESDelta;\n'
        
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
