import os
import FileDirectoryIO.FileManager as IO
import WriteInputFiles.WriteTransportProperties as transport
import WriteInputFiles.WriteTurbulenceProperties as turbulence

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

    # name of the case to use (will be used for the folder name)
    case_name = 'flatPlateTest'

    # path to folder where to copy test case to
    # path = 'D:\\z_dataSecurity\\ubuntu\\OpenFOAM\\run'
    # path = 'C:\\Users\\e802985\\Documents\\openfoam\\run'
    path = ''

    # absolute path of text case location
    case = os.path.join(path, case_name)

    # version of openfoam to use (does not have an influence on the case setup, but will be used in headers)
    version = 'v2006'

    # define boundary conditions
    # first  entry: name of boundary condition (specified in mesh generator)
    # second entry: type of boundary condition
    BC = {
        "inlet": Parameters.INLET,
        "outlet": Parameters.OUTLET,
        "wall": Parameters.WALL,
        "symmetry": Parameters.SYMMETRY,
        "top": Parameters.SYMMETRY,
        "BaseAndTop": Parameters.EMPTY,
    }

    # specify the outlet type
    # NEUMANN     : apply zero gradient neumann boundary condition
    # ADVECTIVE   : transport any fluid outside the domain near outlet (non-reflective boundary condition)
    # INLET_OUTLET: allow for backflow at outlet
    outlet_type = Parameters.NEUMANN

    # specify the inlet boundary condition (free stream velocity)
    inlet_velocity = [1, 0, 0]

    # specify the laminar viscosity
    nu = 1e-4

    # intensity of turbulent kinetic energy (between 0 - 1)
    TKE_intensity = 0.01

    # Reference length in simulation
    reference_length = 2.0

    # Reynolds number calculation
    Re = sqrt(pow(inlet_velocity[0], 2) + pow(inlet_velocity[1], 2) + pow(inlet_velocity[2], 2)) * reference_length / nu

    # simulation type
    # options are: LAMINAR, RANS, LES
    simulation_type = Parameters.RANS

    # use wall functions (if set to false, y+ needs to be in the region of 1, otherwise y+ should be > 30)
    wall_functions = True

    # create the initial data structure for the case set-up
    file_manager = IO.FileManager(case_name, path, version)
    file_manager.create_directory_structure()

    # output velocity boundary conditions
    U.write_boundary_condition(file_manager, BC, outlet_type, inlet_velocity)

    # output pressure boundary conditions
    p.write_boundary_condition(BC, outlet_type, 0, case, version)

    # output turbulent kinetic energy boundary condition
    k.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, wall_functions, case, version)

    # output dissipation rate boundary condition
    epsilon.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, wall_functions, case, version)

    # output specific dissipation rate boundary condition
    omega.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, wall_functions, case, version)

    # output nu tilda boundary conditions
    nuTilda.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, wall_functions, case, version)

    # output turbulent viscosity boundary condition
    nut.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, case, version)

    # write transport properties to file
    transportProperties = transport.TransportPropertiesFile(file_manager, nu)
    transportProperties.write_input_file()

    # write turbulence properties to file
    # Turbulence.write_turbulence_properties(case, version, simulation_type)
    turbulenceProperties = turbulence.TurbulencePropertiesFile(file_manager, simulation_type)
    turbulenceProperties.write_input_file()

    # write control dict file out
    ControlDict.write_control_dict(case, version)

    # write fvSolution file out
    fvSolution.write_fvsolution(case, version)

    # write fvSchemes
    fvSchemes.write_fvschemes(case, version)

    # output diagnostics
    print('Generated case : ' + case)
    print('Reynolds number: ' + str(Re))


if __name__ == '__main__':
    main()