from input.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class LidDrivenCavity(BaseCase):
    """Creates the flow setup for the lid driven cavity example"""

    def __init__(self):
        self.add_parameters('reynolds_number', 1000)
        self.add_parameters('turbulence_type', TurbulenceType.laminar)
        self.add_parameters('RansModel', RansModel.kOmegaSST)

    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'LidDrivenCavity',
                'mesh_treatment': Mesh.block_mesh_dict,
                'blockmeshdict_directory': os.path.join('input', 'mesh', 'lidDrivenCavity'),
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'movingWall': BoundaryConditions.inlet,
                    'fixedWalls': BoundaryConditions.wall,
                    'frontAndBack': BoundaryConditions.empty,
                },
            },
            'flow_properties': {
                'flow_type': FlowType.incompressible,
                'input_parameters_specification_mode': Dimensionality.non_dimensional,
                'non_dimensional_properties': {
                    'Re': self.to_float(BaseCase.parameters['reynolds_number']),
                },
                'axis_aligned_flow_direction': {
                    'tangential': Coordinates.x,
                    'normal': Coordinates.y,
                    'angle_of_attack': 0,
                },
            },
            'solver_properties': {
                'solver': Solver.pimpleFoam,
                'number_of_non_orthogonal_corrector_steps': 0,
                'number_of_corrector_steps': 2,
                'number_of_outer_corrector_steps': 2,
                'pressure_solver': PressureSolver.krylov,
                'under_relaxation_default': 0.7,
            },

            'time_discretisation': {
                'time_integration': TimeTreatment.unsteady,
                'unsteady_properties': {
                    'startFrom': SimulationStart.startTime,
                    'startTime': 0,
                    'endTime': 250,
                    'CFLBasedTimeStepping': True,
                    'CFL': 10.0,
                    'deltaT': 1e-4,
                    'maxDeltaT': 1,
                    'write_control': OutputWriteControl.adjustableRunTime,
                    'write_frequency': 2.0,
                    'purge_write': 0,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': DiscretisationPolicy.default,
                'use_first_order_for_turbulence': True,
            },
            'turbulence_properties': {
                'turbulence_type': self.to_python_expression(BaseCase.parameters['turbulence_type']),
                'turbulent_quantities_at_inlet': TurbulenceLengthScaleCalculation.internal,
                'freestream_turbulent_intensity': 0.05,
                'RansModel': self.to_python_expression(BaseCase.parameters['RansModel']),
            },
            'convergence_control': {
                'convergence_threshold': 1e-6,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-6,
            },

            'dimensionless_coefficients': {
                'reference_length': 1.0,
                'reference_area': 1.0,
                'wall_boundaries': ['fixedWalls'],
                'write_force_coefficients': False,
                'write_pressure_coefficient': False,
                'write_wall_shear_stresses': False,
            },
            'line_probes': {
                'write_line_probes': True,
                'location': [
                    {
                        'name': 'Uy',
                        'start': [0.5, 1, 0.05],
                        'end': [0.5, 0, 0.05],
                    },
                    {
                        'name': 'Vx',
                        'start': [1, 0.5, 0.05],
                        'end': [0, 0.5, 0.05],
                    },
                ],
                'number_of_samples_on_line': 100,
                'variables_to_monitor': ['U'],
                'output_probe_at_every_timestep': False,
            },
            'post_processing': {
                'execute_function_object': True,
                'function_objects': {
                    'calcResiduals': os.path.join('input', 'scripts', 'userDefined', 'functionObjects', 'residuals'),
                },
                'execute_python_script': True,
                'python_script': [
                    {
                        'script': os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                               'lidDrivenCavity', 'plotLidDrivenCavity.py'),
                        'arguments': [self.to_float(BaseCase.parameters['reynolds_number'])],
                        'requires': [
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing', 'lidDrivenCavity',
                                         'Uy.dat'),
                            os.path.join('input', 'scripts', 'userDefined', 'postProcessing', 'lidDrivenCavity',
                                         'Vx.dat'),
                        ],
                    },
                    {
                        'script': os.path.join('input', 'scripts', 'userDefined', 'postProcessing',
                                               'printPerformance.py'),
                        'arguments': [],
                        'requires': [],
                    },
                ],
            },
        })
