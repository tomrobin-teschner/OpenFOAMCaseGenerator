import os
import FileDirectoryIO.FileManager as IO
import WriteConstantDirectoryFiles.WriteTransportProperties as Transport
import WriteConstantDirectoryFiles.WriteTurbulenceProperties as Turbulence

import WriteVelocity as U
import WritePressure as p
import WriteTurbulentKineticEnergy as k
import WriteDissipationRate as epsilon
import WriteSpecificDissipationRate as omega
import WriteNuTilda as nuTilda
import WriteNut as nut
import GlobalVariables as Parameters
import WriteControlDict as ControlDict
import WritefvSolution as fvSolution
import WritefvSchemes as fvSchemes

from math import sqrt, pow


def main():

    # file properties
    file_properties = {
        # name of the case to use (will be used for the folder name)
        'case_name': 'flatPlateTest',

        # path to folder where to copy test case to
        'run_directory': 'D:\\z_dataSecurity\\ubuntu\\OpenFOAM\\run',
        # 'run_directory': 'C:\\Users\\e802985\\Documents\\openfoam\\run',
        # 'run_directory': '',

        # version of openfoam to use (does not have an influence on the case setup, but will be used in headers)
        'version': 'v2006',
    }

    # absolute path of text case location
    file_properties['path'] = os.path.join(file_properties['run_directory'], file_properties['case_name'])

    # define boundary conditions
    # first  entry: name of boundary condition (specified in mesh generator)
    # second entry: type of boundary condition
    boundary_properties = {
        'inlet': Parameters.INLET,
        'outlet': Parameters.OUTLET,
        'wall': Parameters.WALL,
        'symmetry': Parameters.SYMMETRY,
        'top': Parameters.SYMMETRY,
        'BaseAndTop': Parameters.EMPTY,

        # specify the outlet type
        # NEUMANN     : apply zero gradient (neumann) boundary condition (reflective boundary conditions)
        # ADVECTIVE   : transport any fluid outside the domain near outlet (non-reflective boundary condition)
        # INLET_OUTLET: allow for backflow at outlet, prescribe inlet (free-stream) condition for reverse flow
        'outlet_type': Parameters.NEUMANN,
    }

    # physical properties of solver set-up
    flow_properties = {
        # specify the inlet boundary condition (free stream velocity)
        'inlet_velocity': [1, 0, 0],

        # specify the laminar viscosity
        'nu': 1e-4,

        # intensity of turbulent kinetic energy (between 0 - 1)
        'TKE_intensity': 0.01,

        # Reference length in simulation
        'reference_length': 2.0,
    }

    # Reynolds number calculation
    reynolds_number = (
            sqrt(pow(flow_properties['inlet_velocity'][0], 2) +
                 pow(flow_properties['inlet_velocity'][1], 2) +
                 pow(flow_properties['inlet_velocity'][2], 2)) *
            flow_properties['reference_length'] / flow_properties['nu'])
    flow_properties['reynolds_number'] = reynolds_number

    solver_properties = {
        # name of solver to use for simulation
        'solver': 'pimpleFoam',

        # turbulence treatment type
        # options are: LAMINAR, RANS, LES
        'turbulence_type': Parameters.RANS,

        # for RANS only, describe fidelity of wall modelling (i.e. usage of wall functions)
        # LOW_RE  : first cell-height near wall is of order y+ <= 1
        # HIGH_RE : first cell-height near wall is of order y+ >  30
        'wall_modelling': Parameters.LOW_RE,

        # absolute convergence criterion for implicit solvers
        'absolute_convergence_criterion': 1e-8,

        # relative convergence criterion for implicit solvers
        'relative_convergence_criterion': 0.01,

        # convergence criterion for flow solution
        'convergence_threshold': 1e-6,

        # under-relaxation factor for pressure
        'under_relaxation_p': 0.3,

        # under-relxation factor for velocity
        'under_relaxation_U': 0.7,

        # under-relxation factor for turbulent quantities
        'under_relaxation_turbulence': 0.7,
    }

    # create the initial data structure for the case set-up
    file_manager = IO.FileManager(file_properties)
    file_manager.create_directory_structure()

    # output velocity boundary conditions
    U.write_boundary_condition(file_manager, boundary_properties, flow_properties)

    # output pressure boundary conditions
    p.write_boundary_condition(file_manager, boundary_properties, 0)

    # output turbulent kinetic energy boundary condition
    k.write_boundary_condition(file_manager, boundary_properties, flow_properties, solver_properties)

    # output dissipation rate boundary condition
    epsilon.write_boundary_condition(file_manager, boundary_properties, flow_properties, solver_properties)

    # output specific dissipation rate boundary condition
    omega.write_boundary_condition(file_manager, boundary_properties, flow_properties, solver_properties)

    # output nu tilda boundary conditions
    nuTilda.write_boundary_condition(file_manager, boundary_properties, flow_properties, solver_properties)

    # output turbulent viscosity boundary condition
    nut.write_boundary_condition(file_manager, boundary_properties, solver_properties)

    # write transport properties to file
    transportProperties = Transport.TransportPropertiesFile(file_manager, flow_properties)
    transportProperties.write_input_file()

    # write turbulence properties to file
    turbulenceProperties = Turbulence.TurbulencePropertiesFile(file_manager, solver_properties)
    turbulenceProperties.write_input_file()

    # write control dict file out
    ControlDict.write_control_dict(file_manager, solver_properties)

    # write fvSolution file out
    fvSolution.write_fvsolution(file_manager, solver_properties)

    # write fvSchemes
    fvSchemes.write_fvschemes(file_manager)

    # write Allrun file to execute case automatically
    file_manager.write_all_run_file()

    # write Allclean file to clean up case directory
    file_manager.write_all_clean_file()

    # output diagnostics
    print('Generated case : ' + file_properties['path'])
    print('Reynolds number: ' + str(reynolds_number))


if __name__ == '__main__':
    main()