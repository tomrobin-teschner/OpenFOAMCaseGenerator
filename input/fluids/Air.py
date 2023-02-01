from input.fluids.FluidBase import FluidBase


class Air(FluidBase):
    def __init__(self, **kwargs):
        super().__init__()
        self.material_properties['rho'] = 1.225
        self.material_properties['p'] = 101325
        self.material_properties['T'] = 288.15
        self.material_properties['Ts'] = 116
        self.material_properties['mu'] = 1.7894e-5
        self.material_properties['nu'] = 1.46e-5
        self.material_properties['R'] = 287.0
        self.material_properties['gamma'] = 1.4
        self.material_properties['Pr'] = 0.71
        self.material_properties['As'] = 1.4792e-06
        self.material_properties['molWeight'] = 28.9
        self.material_properties['Cp'] = 1005.0
        self.material_properties['Hf'] = 0.0
        
        super().overwrite_default_values(**kwargs)
        super().update_viscosities(**kwargs)