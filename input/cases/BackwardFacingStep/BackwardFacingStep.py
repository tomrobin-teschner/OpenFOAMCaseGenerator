from input.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class BackwardFacingStep(BaseCase):
    """Creates the flow setup for aBackward Facing step simulation for incompressible, turbulent flows"""

    def __init__(self):
        self.add_parameters('custom_inlet_profile', False)
        self.add_parameters('spatial_discretisation', DiscretisationPolicy.default)
        self.add_parameters('turbulence_type', TurbulenceType.rans)
        self.add_parameters('RansModel', RansModel.kOmegaSST)
        self.add_parameters('LesModel', LesModel.kEqn)

    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'BackwardFacingStep',
                'mesh_treatment': Mesh.poly_mesh,
                'polymesh_directory': os.path.join('input', 'mesh', 'backwardFacingStep', 'coarse'),
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'inlet': BoundaryConditions.inlet,
                    'outlet': BoundaryConditions.outlet,
                    'left': BoundaryConditions.cyclic,
                    'right': BoundaryConditions.cyclic,
                    'pre_inlet_bottom': BoundaryConditions.symmetry,
                    'pre_inlet_top': BoundaryConditions.symmetry,
                    'post_inlet_bottom': BoundaryConditions.wall,
                    'post_inlet_top': BoundaryConditions.wall,
                    'bottom_wall': BoundaryConditions.wall,
                    'step': BoundaryConditions.wall,
                },
                'custom_inlet_boundary_conditions': self.to_bool(BaseCase.parameters['custom_inlet_profile']),
                'custom_inlet_boundary_conditions_setup': {
                    'U': os.path.join('input', 'scripts', 'boundaryConditions', 'backwardFacingStep',
                                      'velocityInletProfile'),
                },
            },
            'flow_properties': {
                'flow_type': FlowType.incompressible,
                'input_parameters_specification_mode': Dimensionality.dimensional,
                'dimensional_properties': {
                    'material': MaterialProperty.Air,
                    'material_properties': {
                        'rho': 1.0,
                        'nu': 1.0e-4,
                    },
                    'velocity': [3.410896, 0.0, 0.0],
                },
            },
            'solver_properties': {
                'solver': Solver.pimpleFoam,
                'number_of_non_orthogonal_corrector_steps': 0,
                'number_of_corrector_steps': 1,
                'number_of_outer_corrector_steps': 1,
                'pressure_solver': PressureSolver.multi_grid,
                'under_relaxation_default': 0.7,
            },
            'time_discretisation': {
                'time_integration': TimeTreatment.steady_state,
                'steady_state_properties': {
                    'startFrom': SimulationStart.startTime,
                    'startTime': 0,
                    'endTime': 2000,
                    'CFLBasedTimeStepping': False,
                    'CFL': 1.0,
                    'deltaT': 1,
                    'maxDeltaT': 1,
                    'write_control': OutputWriteControl.timeStep,
                    'write_frequency': 100,
                    'purge_write': 0,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': self.to_python_expression(BaseCase.parameters['spatial_discretisation']),
                'use_first_order_for_turbulence': True,
            },
            'turbulence_properties': {
                'turbulence_type': self.to_python_expression(BaseCase.parameters['turbulence_type']),
                'wall_modelling': WallModelling.low_re,
                'turbulent_quantities_at_inlet': TurbulenceLengthScaleCalculation.internal,
                'freestream_turbulent_intensity': 0.05,
                'RansModel': self.to_python_expression(BaseCase.parameters['RansModel']),
                'LesModel': self.to_python_expression(BaseCase.parameters['LesModel']),
                'LesFilter': LesFilter.simple,
                'DeltaModel': DeltaModel.cubeRootVol,
            },
            'convergence_control': {
                'convergence_threshold': 1e-6,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-4,
                'integral_convergence_criterion': [IntegralQuantities.Cd],
                'averaging_time_steps': 20,
                'integral_quantities_convergence_threshold': 1e-8,
                'time_steps_to_wait_before_checking_convergence': 10,
            },
            'dimensionless_coefficients': {
                'reference_length': 1.0,
                'reference_area': 50.0,
                'wall_boundaries': ['bottom_wall'],
                'write_force_coefficients': True,
                'write_pressure_coefficient': False,
                'write_wall_shear_stresses': True,
            },
            'point_probes': {
                'write_point_probes': True,
                'location': [
                    [-4, -0.5, 5],
                ],
                'variables_to_monitor': ['U'],
                'output_probe_at_every_timestep': True,
            },
            'line_probes': {
                'write_line_probes': True,
                'location': [
                    {
                        'name': 'x_by_H=-4',
                        'start': [-4.0, -0.5, 1.0],
                        'end': [-4.0, -0.5, 9.0],
                    },
                    {
                        'name': 'x_by_H=1',
                        'start': [1, -0.5, 0.0],
                        'end': [1, -0.5, 9.0],
                    },
                    {
                        'name': 'x_by_H=4',
                        'start': [4, -0.5, 0.0],
                        'end': [4, -0.5, 9.0],
                    },
                    {
                        'name': 'x_by_H=6',
                        'start': [6, -0.5, 0.0],
                        'end': [6, -0.5, 9.0],
                    },
                    {
                        'name': 'x_by_H=10',
                        'start': [10, -0.5, 0.0],
                        'end': [10, -0.5, 9.0],
                    },
                    {
                        'name': 'bottom_wall',
                        'start': [0, -0.5, 0.0],
                        'end': [50, -0.5, 0.0],
                    },
                ],
                'number_of_samples_on_line': 1000,
                'variables_to_monitor': ['U', 'wallShearStress'],
                'output_probe_at_every_timestep': False,
            },
            'post_processing': {
                'execute_python_script': True,
                'python_script': [
                    {
                        'script': os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                               'backwardFacingStep', 'plotBackwardFacingStep.py'),
                        'arguments': [''],
                        'requires': [
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                         'backwardFacingStep', 'experimental_cf_data.csv'),
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                         'backwardFacingStep', 'x_by_H=-4.csv'),
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                         'backwardFacingStep', 'x_by_H=1.csv'),
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                         'backwardFacingStep', 'x_by_H=4.csv'),
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                         'backwardFacingStep', 'x_by_H=6.csv'),
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                         'backwardFacingStep', 'x_by_H=10.csv'),
                        ],
                    },
                ],
            },
        })
