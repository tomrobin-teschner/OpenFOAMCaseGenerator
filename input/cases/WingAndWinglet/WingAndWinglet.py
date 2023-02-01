from input.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class WingAndWinglet(BaseCase):
    """Creates the input for a wing with winglet simulation"""

    def __init__(self):
        self.add_parameters('angle_of_attack', 5)

    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'WingAndWinglet',
                'mesh_treatment': Mesh.snappy_hex_mesh_dict,
                'snappyhexmeshdict': {
                    'snappyhexmesh_directory': os.path.join('input', 'mesh', 'wing_and_winglet'),
                    'blockmeshdict_directory': os.path.join('input', 'mesh', 'wing_and_winglet'),
                    'polymesh_directory': os.path.join(''),
                    'geometry': [
                        os.path.join('input', 'geometry', 'wing_and_winglet', 'wing_and_winglet.stl'),
                    ]
                },
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'wing_and_winglet': BoundaryConditions.wall,
                    'symmetry': BoundaryConditions.symmetry,
                    'inlet': BoundaryConditions.freestream,
                    'outlet': BoundaryConditions.freestream,
                },
            },
            'flow_properties': {
                'flow_type': FlowType.incompressible,
                'const_viscosity': True,
                'input_parameters_specification_mode': Dimensionality.dimensional,
                'dimensional_properties': {
                    'material': MaterialProperty.Air,
                    'material_properties': {
                        'p': 0,
                    },
                    'velocity_magnitude': 10,
                },
                'axis_aligned_flow_direction': {
                    'tangential': Coordinates.x,
                    'normal': Coordinates.y,
                    'angle_of_attack': self.to_float(BaseCase.parameters['angle_of_attack']),
                },
            },
            'solver_properties': {
                'solver': Solver.pimpleFoam,
                'number_of_non_orthogonal_corrector_steps': 2,
                'number_of_corrector_steps': 2,
                'number_of_outer_corrector_steps': 1,
                'pressure_solver': PressureSolver.krylov,
                'under_relaxation_default': 0.7,
            },
            'time_discretisation': {
                'time_integration': TimeTreatment.steady_state,
                'steady_state_properties': {
                    'startFrom': SimulationStart.startTime,
                    'startTime': 0,
                    'endTime': 2000,
                    'CFLBasedTimeStepping': False,
                    'deltaT': 1,
                    'write_control': OutputWriteControl.timeStep,
                    'write_frequency': 250,
                    'purge_write': 0,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': DiscretisationPolicy.default,
                'use_first_order_for_turbulence': True,
            },
            'turbulence_properties': {
                'turbulence_type': TurbulenceType.rans,
                'wall_modelling': WallModelling.high_re,
                'turbulent_quantities_at_inlet': TurbulenceLengthScaleCalculation.external,
                'freestream_turbulent_intensity': 0.0005,
                'RansModel': RansModel.kOmegaSST,
            },
            'convergence_control': {
                'convergence_threshold': 1e-6,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-4,
                'integral_convergence_criterion': [IntegralQuantities.Cd, IntegralQuantities.Cl],
                'averaging_time_steps': 20,
                'integral_quantities_convergence_threshold': 1e-5,
                'time_steps_to_wait_before_checking_convergence': 10,
            },
            'dimensionless_coefficients': {
                'reference_length': 0.34,
                'reference_area': 0.326,
                'center_of_rotation': [0.085, 0, 0],
                'wall_boundaries': ['wing_and_winglet'],
                'write_force_coefficients': True,
                'write_pressure_coefficient': True,
                'write_wall_shear_stresses': False,
            },
        })
