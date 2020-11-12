import os
import FileManager as file_manager
import WriteVelocity as U
import WritePressure as p
import WriteTurbulentKineticEnergy as k
import WriteDissipationRate as epsilon
import WriteSpecificDissipationRate as omega
import WriteNuTilda as nuTilda
import WriteNut as nut
import GlobalVariables as Parameters
import WriteTransportProperties as Transport
import WriteTurbulenceProperties as Turbulence

from math import sqrt, pow


def main():
    # name of the case to use (will be used for the folder name)
    case_name = 'test_case'

    # path to folder where to copy test case to
    path = 'C:\\Users\\e802985\\Documents\\openfoam\\run'

    # absolute path of text case location
    case = os.path.join(path, case_name)

    # version of openfoam to use (does not have an influence on the case setup, but will be used in headers)
    version = 'v1912'

    # define boundary conditions
    # first  entry: name of boundary condition (specified in mesh generator
    # second entry: type of boundary condition
    BC = {
        "inlet": Parameters.INLET,
        "outflow": Parameters.OUTLET,
        "wall": Parameters.WALL,
        "symmetry": Parameters.SYMMETRY,
        "top": Parameters.SYMMETRY,
        "frontAndBack": Parameters.EMPTY,
        "left": Parameters.CYCLIC,
        "right": Parameters.CYCLIC
    }

    # specify the outlet type
    # NEUMANN     : apply zero gradient neumann boundary condition
    # ADVECTIVE   : transport any fluid outside the domain near outlet (non-reflective boundary condition)
    # INLET_OUTLET: allow for backflow at outlet
    outlet_type = Parameters.NEUMANN

    # specify the inlet boundary condition (free stream velocity)
    inlet_velocity = [10, 0, 0]

    # specify the laminar viscosity
    nu = 1e-4

    # intensity of turbulent kinetic energy (between 0 - 1)
    TKE_intensity = 0.05

    # Reference length in simulation
    reference_length = 1.0

    # Reynolds number calculation
    Re = sqrt(pow(inlet_velocity[0], 2) + pow(inlet_velocity[1], 2) + pow(inlet_velocity[2], 2)) * reference_length / nu

    # simulation type
    # options are: LAMINAR, RANS, LES
    simulation_type = Parameters.RANS

    # use wall functions (if set to false, y+ needs to be in the region of 1, otherwise y+ should be > 30)
    wall_functions = True

    # file output writing
    file_manager.create_folder(case)

    # output velocity boundary conditions
    U.write_boundary_condition(BC, outlet_type, inlet_velocity, case, version)

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
    Transport.write_transport_properties(case, version, nu)

    # write turbulence properties to file
    Turbulence.write_turbulence_properties(case, version, simulation_type)

    # output diagnostics
    print('Generated case : ' + case)
    print('Reynolds number: ' + str(Re))


if __name__ == '__main__':
    main()