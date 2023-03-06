from input.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class Naca0012(BaseCase):
    """Creates the flow setup for a NACA 0012 aerofoil simulation"""

    def __init__(self):
        self.add_parameters('reynolds_number', 6000000)
        self.add_parameters('angle_of_attack', 0)
        self.add_parameters('rans_model', RansModel.kOmegaSST)
        self.add_parameters('mesh', 'coarse')

    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'Naca0012',
                'mesh_treatment': Mesh.poly_mesh,
                'polymesh_directory': os.path.join('input', 'mesh', 'airfoilNASA', BaseCase.parameters['mesh']),
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'airfoil': BoundaryConditions.wall,
                    'farfield': BoundaryConditions.freestream,
                    'BaseAndTop': BoundaryConditions.empty,
                },
            },
            'flow_properties': {
                'flow_type': FlowType.incompressible,
                'const_viscosity': True,
                'input_parameters_specification_mode': Dimensionality.non_dimensional,
                'non_dimensional_properties': {
                    'Re': self.to_float(BaseCase.parameters['reynolds_number']),
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
                'number_of_outer_corrector_steps': 2,
                'under_relaxation_equations': {
                    'U': 0.7,
                },
            },
            'time_discretisation': {
                'time_integration': TimeTreatment.unsteady,
                'unsteady_properties': {
                    'startFrom': SimulationStart.startTime,
                    'startTime': 0,
                    'endTime': 500,
                    'CFLBasedTimeStepping': True,
                    'CFL': 2500.0,
                    'deltaT': 1e-4,
                    'maxDeltaT': 1,
                    'write_control': OutputWriteControl.adjustableRunTime,
                    'write_frequency': 10,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': DiscretisationPolicy.default,
                'use_first_order_for_turbulence': True,
            },
            'turbulence_properties': {
                'turbulence_type': TurbulenceType.rans,
                'wall_modelling': WallModelling.low_re,
                'turbulent_quantities_at_inlet': TurbulenceLengthScaleCalculation.external,
                'freestream_turbulent_intensity': 0.00052,
                'RansModel': self.to_python_expression(BaseCase.parameters['rans_model']),
            },
            'convergence_control': {
                'convergence_threshold': 1e-6,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-4,
                'integral_convergence_criterion': [IntegralQuantities.Cd, IntegralQuantities.Cl],
                'averaging_time_steps': 20,
                'integral_quantities_convergence_threshold': 1e-5,
                'time_steps_to_wait_before_checking_convergence': 0.001,
            },
            'dimensionless_coefficients': {
                'reference_length': 1.0,
                'reference_area': 1.0,
                'center_of_rotation': [0.25, 0, 0],
                'wall_boundaries': ['airfoil'],
                'write_force_coefficients': True,
                'write_pressure_coefficient': True,
                'write_wall_shear_stresses': False,
            },
        })