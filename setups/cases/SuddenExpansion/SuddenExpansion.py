from setups.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class SuddenExpansion(BaseCase):
    """Creates the flow setup for a suddenly expanding channel to test flow bifurcation"""
    parameters = {
        'reynolds_number': 80,
    }

    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'SuddenExpansion',
                'mesh_treatment': Mesh.block_mesh_dict,
                'blockmeshdict_directory': os.path.join('setups', 'mesh', 'suddenExpansion'),
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'inlet': BoundaryConditions.inlet,
                    'outlet': BoundaryConditions.outlet,
                    'channelAndStep': BoundaryConditions.wall,
                    'bottom': BoundaryConditions.wall,
                    'top': BoundaryConditions.wall,
                    'frontAndBack': BoundaryConditions.empty,
                },
            },
            'flow_properties': {
                'custom_initial_conditions': True,
                'custom_initial_conditions_setup': {
                    'U': os.path.join('setups', 'scripts', 'initialConditions', 'suddenExpansion', 'U'),
                },
                'flow_type': FlowType.incompressible,
                'input_parameters_specification_mode': Dimensionality.non_dimensional,
                'non_dimensional_properties': {
                    'Re': self.to_float(SuddenExpansion.parameters['reynolds_number']),
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
                'number_of_outer_corrector_steps': 1,
                'pressure_solver': PressureSolver.krylov,
                'under_relaxation_default': 0.7,
            },

            'time_discretisation': {
                'time_integration': TimeTreatment.unsteady,
                'unsteady_properties': {
                    'startFrom': SimulationStart.startTime,
                    'startTime': 0,
                    'endTime': 50,
                    'CFLBasedTimeStepping': True,
                    'CFL': 10.0,
                    'deltaT': 1e-4,
                    'maxDeltaT': 1,
                    'write_control': OutputWriteControl.adjustableRunTime,
                    'write_frequency': 1,
                    'purge_write': 0,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': DiscretisationPolicy.accuracy,
                'use_first_order_for_turbulence': True,
            },
            'turbulence_properties': {
                'turbulence_type': TurbulenceType.laminar,
            },
            'convergence_control': {
                'convergence_threshold': 1e-6,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-6,
            },
            'line_probes': {
                'write_line_probes': True,
                'location': [
                    {
                        'name': 'x_by_h=1_25',
                        'start': [1.25, -1.5, 0.0],
                        'end':   [1.25,  1.5, 0.0],
                    },
                    {
                        'name': 'x_by_h=2_5',
                        'start': [2.5, -1.5, 0.0],
                        'end':   [2.5,  1.5, 0.0],
                    },
                    {
                        'name': 'x_by_h=5_0',
                        'start': [5.0, -1.5, 0.0],
                        'end':   [5.0,  1.5, 0.0],
                    },
                    {
                        'name': 'x_by_h=10_0',
                        'start': [10.0, -1.5, 0.0],
                        'end':   [10.0,  1.5, 0.0],
                    },
                ],
                'number_of_samples_on_line': 100,
                'variables_to_monitor': ['U'],
                'output_probe_at_every_timestep': False,
            },
            'post_processing': {
                'execute_python_script': False,
                'python_script': [
                    {
                        'script': os.path.join(''),
                        'arguments': [''],
                        'requires': [
                            os.path.join(''),
                        ],
                    },
                ],
            },
        })
