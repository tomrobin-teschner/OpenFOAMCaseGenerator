from abc import ABC


class FluidBase(ABC):
    '''This class describes the base properties of a fluid'''
    def __init__(self, **kwargs):
        self.material_properties = {
            'rho': float(),
            'p': float(),
            'T': float(),
            'Ts': float(),
            'mu': float(),
            'nu': float(),
            'R': float(),
            'gamma': float(),
            'Pr': float(),
            'As': float(),
            'molWeight': float(),
            'Cp': float(),
            'Hf': float()
        }

    def overwrite_default_values(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.material_properties:
                self.material_properties[key] = value

    def update_viscosities(self, **kwargs):
        '''esnure that if either rho, nu, mu, or a combination of them is given that viscosities are up to date'''
        if 'mu' in kwargs.keys() and 'rho' in kwargs.keys() and 'nu' not in kwargs.keys():
            self.material_properties['nu'] = kwargs['mu'] / kwargs['rho']
        elif 'nu' in kwargs.keys() and 'mu' in kwargs.keys() and 'rho' not in kwargs.keys():
            self.material_properties['rho'] = kwargs['mu'] / kwargs['nu']
        elif 'rho' in kwargs.keys() and 'nu' in kwargs.keys() and 'mu' not in kwargs.keys():
            self.material_properties['mu'] = kwargs['rho'] * kwargs['nu']
        elif 'rho' in kwargs.keys() and 'nu' not in kwargs.keys() and 'mu' not in kwargs.keys():
            self.material_properties['nu'] = self.material_properties['mu'] / kwargs['rho']
        elif 'mu' in kwargs.keys() and 'rho' not in kwargs.keys() and 'nu' not in kwargs.keys():
            self.material_properties['nu'] = kwargs['mu'] / self.material_properties['rho']
        elif 'nu' in kwargs.keys() and 'rho' not in kwargs.keys() and 'mu' not in kwargs.keys():
            self.material_properties['mu'] = self.material_properties['rho'] * kwargs['nu']

    def get(self, key):
        if key in self.material_properties:
            return self.material_properties[key]
        else:
            raise Exception(f'Could not find {key} in material properties')

    def set(self, key, value):
        if key in self.material_properties:
            self.material_properties[key] = value
        else:
            raise Exception(f'Could not find {key} in material properties')