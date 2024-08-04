from input.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class Cylinder(BaseCase):
    """Creates the flow setup for an unsteady flow around a cylinder"""
    
    def __init__(self):
        pass
    
    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'cylinder',
                'mesh_treatment': Mesh.poly_mesh,
                'polymesh_directory': os.path.join('input', 'mesh', 'cylinder'),
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'cylinder': BoundaryConditions.wall,
                    'freestream': BoundaryConditions.freestream,
                    'outlet': BoundaryConditions.advective_outlet,
                    'BaseAndTop': BoundaryConditions.empty,
                },
            },
            'flow_properties': {
                'custom_initial_conditions': True,
                'custom_initial_conditions_setup': {
                    'variable': os.path.join('input', 'scripts', 'initialConditions', 'cylinder', 'U'),
                },
                'flow_type': FlowType.incompressible,
                'const_viscosity': True,
                'input_parameters_specification_mode': Dimensionality.dimensional,
                'dimensional_properties': {
                    'material': MaterialProperty.Air,
                    'material_properties': {
                        'nu': 0.01,
                    },
                    'velocity': [1.0, 0.0, 0.0],
                },
            },
            'solver_properties': {
                'solver': Solver.pimpleFoam,
                'number_of_non_orthogonal_corrector_steps': 1,
                'number_of_corrector_steps': 1,
                'number_of_outer_corrector_steps': 10,
                'pressure_solver': PressureSolver.multi_grid,
                'under_relaxation_default': 0.7,
            },

            'time_discretisation': {
                'time_integration': TimeTreatment.unsteady,
                'unsteady_properties': {
                    'startFrom': SimulationStart.startTime,
                    'startTime': 0,
                    'endTime': 100,
                    'CFLBasedTimeStepping': True,
                    'CFL': 10.0,
                    'deltaT': 0.5,
                    'maxDeltaT': 1,
                    'write_control': OutputWriteControl.adjustableRunTime,
                    'write_frequency': 0.5,
                    'purge_write': 0,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': DiscretisationPolicy.default,
                'use_first_order_for_turbulence': False,
            },
            'turbulence_properties': {
                'turbulence_type': TurbulenceType.laminar,
            },
            'convergence_control': {
                'convergence_threshold': 1e-6,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-6,
            },
            'dimensionless_coefficients': {
                'reference_length': 1.0,
                'reference_area': 1.0,
                'center_of_rotation': [0, 0, 0],
                'wall_boundaries': ['cylinder'],
                'write_force_coefficients': True,
                'write_pressure_coefficient': False,
                'write_wall_shear_stresses': True,
            },
        })
