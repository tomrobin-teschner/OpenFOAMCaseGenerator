from setups.cases.BaseCase.BaseCase import *
from src.CaseGenerator.Properties.GlobalVariables import *
import os


class TaylorGreenVortex(BaseCase):
    """Creates the case setup for the Taylor-Green Vortex problem"""
    parameters = {
        'flow_type': FlowType.compressible,
        'solver': Solver.rhoPimpleFoam,
    }

    def create_case(self):
        self.update_case({
            'file_properties': {
                'case_name': 'TaylorGreenVortex',
                'mesh_treatment': Mesh.block_mesh_dict,
                'blockmeshdict_directory': os.path.join('setups', 'mesh', 'TaylorGreenVortex'),
                'run_directory': os.path.join(''),
                'version': 'v2212',
            },
            'parallel_properties': {
                'run_in_parallel': True,
                'number_of_processors': 4,
            },
            'boundary_properties': {
                'boundary_conditions': {
                    'top': BoundaryConditions.cyclic,
                    'bottom': BoundaryConditions.cyclic,
                    'left': BoundaryConditions.cyclic,
                    'right': BoundaryConditions.cyclic,
                    'front': BoundaryConditions.cyclic,
                    'back': BoundaryConditions.cyclic,
                },
            },
            'flow_properties': {
                'custom_initial_conditions': True,
                'custom_initial_conditions_setup': {
                    'p': os.path.join('setups', 'scripts', 'initialConditions', 'TaylorGreenVortex', 'compressible',
                                      'p'),
                    'U': os.path.join('setups', 'scripts', 'initialConditions', 'TaylorGreenVortex', 'compressible',
                                      'U'),
                },
                'flow_type': self.to_python_expression(TaylorGreenVortex.parameters['flow_type']),
                'const_viscosity': True,
                'input_parameters_specification_mode': Dimensionality.dimensional,
                'dimensional_properties': {
                    'velocity_magnitude': 1.0,
                    'rho': 1.0,
                    'nu': 6.25e-4,
                    'p': 100,
                    'T': 300,
                },
            },
            'solver_properties': {
                'solver': self.to_python_expression(TaylorGreenVortex.parameters['solver']),
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
                    'endTime': 20,
                    'CFLBasedTimeStepping': False,
                    'deltaT': 1e-2,
                    'write_control': OutputWriteControl.timeStep,
                    'write_frequency': 50,
                    'purge_write': 0,
                },
            },
            'spatial_discretisation': {
                'numerical_schemes_correction': DiscretisationPolicy.accuracy,
                'use_first_order_for_turbulence': True,
            },
            'turbulence_properties': {
                'turbulence_type': TurbulenceType.les,
                'LesModel': LesModel.kEqn,
                'LesFilter': LesFilter.simple,
                'DeltaModel': DeltaModel.cubeRootVol,
            },
            'convergence_control': {
                'convergence_threshold': 0,
                'absolute_convergence_criterion': 1e-14,
                'relative_convergence_criterion': 1e-6,
            },
            'additional_fields': {
                'write_additional_fields': True,
                'fields': [Fields.q, Fields.vorticity],
            },
            'cutting_planes': {
                'write_cutting_planes': True,
                'location': [
                    {
                        'name': 'plane_x=0',
                        'origin': [0, 0, 0],
                        'normal': [1, 0, 0],
                    },
                    {
                        'name': 'plane_y=0',
                        'origin': [0, 0, 0],
                        'normal': [0, 1, 0],
                    },
                    {
                        'name': 'plane_z=0',
                        'origin': [0, 0, 0],
                        'normal': [0, 0, 1],
                    },
                ],
                'variables_to_monitor': ['U', 'p', 'vorticity'],
                'output_cutting_plane_at_every_timestep': False,
            },
            'iso_surfaces': {
                'write_iso_surfaces': True,
                'flow_variable': ['Q'],
                'iso_value': [0.1],
                'additional_field_to_write': ['p'],
                'output_iso_surfaces_at_every_timestep': False,
            },
            'post_processing': {
                'execute_function_object': True,
                'function_objects': {
                    'turbulenceStatistics': os.path.join('setups', 'scripts', 'userDefined', 'functionObjects',
                                                            'TaylorGreenVortex')
                },
                'execute_python_script': True,
                'python_script': [
                    {
                        'script': os.path.join('setups', 'scripts', 'userDefined', 'postProcessing',
                                               'TaylorGreenVortex', 'plotTaylorGreenVortex.py'),
                        'arguments': [''],
                        'requires': [
                            os.path.join('setups', 'scripts', 'userDefined', 'postProcessing',
                                         'TaylorGreenVortex', 'taylor_green_vortex_512_ref.dat'),
                        ],
                    },
                ],
            },
        })
