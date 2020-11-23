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
                self.file_manager.write(file_id, 'RAS\n{\n')
                if self.turbulence_properties['turbulence_model'] == Parameters.kEpsilon:
                    self.file_manager.write(file_id, '    RASModel        kEpsilon;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.realizableKE:
                    self.file_manager.write(file_id, '    RASModel        realizableKE;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.RNGkEpsilon:
                    self.file_manager.write(file_id, '    RASModel        RNGkEpsilon;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.LienLeschziner:
                    self.file_manager.write(file_id, '    RASModel        LienLeschziner;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.LamBremhorstKE:
                    self.file_manager.write(file_id, '    RASModel        LamBremhorstKE;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.LaunderSharmaKE:
                    self.file_manager.write(file_id, '    RASModel        LaunderSharmaKE;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.kOmega:
                    self.file_manager.write(file_id, '    RASModel        kOmega;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.kOmegaSST:
                    self.file_manager.write(file_id, '    RASModel        kOmegaSST;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.kOmegaSSTLM:
                    self.file_manager.write(file_id, '    RASModel        kOmegaSSTLM;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.kkLOmega:
                    self.file_manager.write(file_id, '    RASModel        kkLOmega;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.qZeta:
                    self.file_manager.write(file_id, '    RASModel        qZeta;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.SpalartAllmaras:
                    self.file_manager.write(file_id, '    RASModel        SpalartAllmaras;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.LienCubicKE:
                    self.file_manager.write(file_id, '    RASModel        LienCubicKE;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.ShihQuadraticKE:
                    self.file_manager.write(file_id, '    RASModel        ShihQuadraticKE;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.LRR:
                    self.file_manager.write(file_id, '    RASModel        LRR;\n')
                elif self.turbulence_properties['turbulence_model'] == Parameters.SSG:
                    self.file_manager.write(file_id, '    RASModel        SSG;\n')
                self.file_manager.write(file_id, '\n')
                self.file_manager.write(file_id, '    turbulence      on;\n')
                self.file_manager.write(file_id, '\n')
                self.file_manager.write(file_id, '    printCoeffs     on;\n')
            if self.turbulence_properties['turbulence_type'] == Parameters.LES:
                self.file_manager.write(file_id, 'LES\n{\n')
                self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '}\n\n')
        self.file_manager.write(file_id, '// ************************************************************************* //\n')
        self.file_manager.close_file(file_id)
