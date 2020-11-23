import GlobalVariables as Parameters


class TurbulencePropertiesFile:
    def __init__(self, file_manager, turbulence_properties):
        self.file_manager = file_manager
        self.turbulence_properties = turbulence_properties

    def write_input_file(self):
        file_id = self.file_manager.create_file('constant', 'turbulenceProperties')
        self.file_manager.write_header(file_id, 'dictionary', 'constant', 'turbulenceProperties')
        self.file_manager.write(file_id, '\n')
        if self.turbulence_properties['turbulence_type'] == Parameters.LAMINAR:
            self.file_manager.write(file_id, 'simulationType laminar;\n')
        elif self.turbulence_properties['turbulence_type'] == Parameters.RANS:
            self.file_manager.write(file_id, 'simulationType RAS;\n')
        elif self.turbulence_properties['turbulence_type'] == Parameters.LES:
            self.file_manager.write(file_id, 'simulationType LES;\n')
        self.file_manager.write(file_id, '\n')
        if self.turbulence_properties['turbulence_type'] != Parameters.LAMINAR:
            if self.turbulence_properties['turbulence_type'] == Parameters.RANS:
                self.__write_RANS(file_id)
            if self.turbulence_properties['turbulence_type'] == Parameters.LES:
                self.__write_LES(file_id)
        self.file_manager.write(file_id, '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)

    def __write_RANS(self, file_id):
        self.file_manager.write(file_id, 'RAS\n{\n')
        if self.turbulence_properties['RANS_model'] == Parameters.kEpsilon:
            self.file_manager.write(file_id, '    RASModel        kEpsilon;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.realizableKE:
            self.file_manager.write(file_id, '    RASModel        realizableKE;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.RNGkEpsilon:
            self.file_manager.write(file_id, '    RASModel        RNGkEpsilon;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.LienLeschziner:
            self.file_manager.write(file_id, '    RASModel        LienLeschziner;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.LamBremhorstKE:
            self.file_manager.write(file_id, '    RASModel        LamBremhorstKE;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.LaunderSharmaKE:
            self.file_manager.write(file_id, '    RASModel        LaunderSharmaKE;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.kOmega:
            self.file_manager.write(file_id, '    RASModel        kOmega;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.kOmegaSST:
            self.file_manager.write(file_id, '    RASModel        kOmegaSST;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.kOmegaSSTLM:
            self.file_manager.write(file_id, '    RASModel        kOmegaSSTLM;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.kkLOmega:
            self.file_manager.write(file_id, '    RASModel        kkLOmega;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.qZeta:
            self.file_manager.write(file_id, '    RASModel        qZeta;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.SpalartAllmaras:
            self.file_manager.write(file_id, '    RASModel        SpalartAllmaras;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.LienCubicKE:
            self.file_manager.write(file_id, '    RASModel        LienCubicKE;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.ShihQuadraticKE:
            self.file_manager.write(file_id, '    RASModel        ShihQuadraticKE;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.LRR:
            self.file_manager.write(file_id, '    RASModel        LRR;\n')
        elif self.turbulence_properties['RANS_model'] == Parameters.SSG:
            self.file_manager.write(file_id, '    RASModel        SSG;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    turbulence      on;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    printCoeffs     on;\n')
        self.file_manager.write(file_id, '}\n\n')

    def __write_LES(self, file_id):
        self.file_manager.write(file_id, 'LES\n{\n')
        if self.turbulence_properties['LES_model'] == Parameters.Smagorinsky:
            self.file_manager.write(file_id, '    LESModel        Smagorinsky;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.kEqn:
            self.file_manager.write(file_id, '    LESModel        kEqn;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.dynamicKEqn:
            self.file_manager.write(file_id, '    LESModel        dynamicKEqn;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.dynamicLagrangian:
            self.file_manager.write(file_id, '    LESModel        dynamicLagrangian;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.DeardorffDiffStress:
            self.file_manager.write(file_id, '    LESModel        DeardorffDiffStress;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.WALE:
            self.file_manager.write(file_id, '    LESModel        WALE;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.SpalartAllmarasDES:
            self.file_manager.write(file_id, '    LESModel        SpalartAllmarasDES;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.SpalartAllmarasDDES:
            self.file_manager.write(file_id, '    LESModel        SpalartAllmarasDDES;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.SpalartAllmarasIDDES:
            self.file_manager.write(file_id, '    LESModel        SpalartAllmarasIDDES;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.kOmegaSSTDES:
            self.file_manager.write(file_id, '    LESModel        kOmegaSSTDES;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.kOmegaSSTDDES:
            self.file_manager.write(file_id, '    LESModel        kOmegaSSTDDES;\n')
        elif self.turbulence_properties['LES_model'] == Parameters.kOmegaSSTIDDES:
            self.file_manager.write(file_id, '    LESModel        kOmegaSSTIDDES;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    turbulence      on;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    printCoeffs     on;\n')
        self.file_manager.write(file_id, '\n')
        if self.turbulence_properties['delta_model'] == Parameters.smooth:
            self.file_manager.write(file_id, '    delta           smooth;\n')
        elif self.turbulence_properties['delta_model'] == Parameters.Prandtl:
            self.file_manager.write(file_id, '    delta           Prandtl;\n')
        elif self.turbulence_properties['delta_model'] == Parameters.maxDeltaxyz:
            self.file_manager.write(file_id, '    delta           maxDeltaxyz;\n')
        elif self.turbulence_properties['delta_model'] == Parameters.cubeRootVol:
            self.file_manager.write(file_id, '    delta           cubeRootVol;\n')
        elif self.turbulence_properties['delta_model'] == Parameters.maxDeltaxyzCubeRoot:
            self.file_manager.write(file_id, '    delta           maxDeltaxyzCubeRoot;\n')
        elif self.turbulence_properties['delta_model'] == Parameters.vanDriest:
            self.file_manager.write(file_id, '    delta           vanDriest;\n')
        elif self.turbulence_properties['delta_model'] == Parameters.IDDESDelta:
            self.file_manager.write(file_id, '    delta           IDDESDelta;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    cubeRootVolCoeffs\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        deltaCoeff        1;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    PrandtlCoeffs\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        delta           cubeRootVol;\n')
        self.file_manager.write(file_id, '        cubeRootVolCoeffs\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            deltaCoeff      1;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '        smoothCoeffs\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            delta           cubeRootVol;\n')
        self.file_manager.write(file_id, '            cubeRootVolCoeffs\n')
        self.file_manager.write(file_id, '            {\n')
        self.file_manager.write(file_id, '                deltaCoeff      1;\n')
        self.file_manager.write(file_id, '            }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '            maxDeltaRatio   1.1;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '        Cdelta          0.158;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    vanDriestCoeffs\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        delta           cubeRootVol;\n')
        self.file_manager.write(file_id, '        cubeRootVolCoeffs\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            deltaCoeff      1;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '        smoothCoeffs\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            delta           cubeRootVol;\n')
        self.file_manager.write(file_id, '            cubeRootVolCoeffs\n')
        self.file_manager.write(file_id, '            {\n')
        self.file_manager.write(file_id, '                deltaCoeff      1;\n')
        self.file_manager.write(file_id, '            }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '            maxDeltaRatio   1.1;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '        Aplus           26;\n')
        self.file_manager.write(file_id, '        Cdelta          0.158;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    smoothCoeffs\n')
        self.file_manager.write(file_id, '    {\n')
        self.file_manager.write(file_id, '        delta           cubeRootVol;\n')
        self.file_manager.write(file_id, '        cubeRootVolCoeffs\n')
        self.file_manager.write(file_id, '        {\n')
        self.file_manager.write(file_id, '            deltaCoeff      1;\n')
        self.file_manager.write(file_id, '        }\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '        maxDeltaRatio   1.1;\n')
        self.file_manager.write(file_id, '    }\n')
        self.file_manager.write(file_id, '}\n\n')
