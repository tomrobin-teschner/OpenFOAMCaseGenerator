import os
import WriteVelocity as U
import WritePressure as p
import WriteTurbulentKineticEnergy as k
import WriteDissipationRate as epsilon
import WriteSpecificDissipationRate as omega
import WriteNuTilda as nuTilda
import WriteNut as nut
import GlobalVariables as Parameters


def main():
    # name of the case to use (will be used for the folder name)
    case_name = 'test_case'

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

    # intensity of turbulent kinetic energy (between 0 - 1)
    TKE_intensity = 0.05

    # Reference length in simulation
    reference_length = 1.0

    # use wall functions (if set to false, y+ needs to be in the region of 1)
    wall_functions = True

    # file output writing
    create_folder(case_name)

    # output velocity boundary conditions
    U.write_boundary_condition(BC, outlet_type, inlet_velocity, case_name, version)

    # output pressure boundary conditions
    p.write_boundary_condition(BC, outlet_type, 0, case_name, version)

    # output turbulent kinetic energy boundary condition
    k.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, wall_functions, case_name, version)

    # output dissipation rate boundary condition
    epsilon.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, wall_functions, case_name, version)

    # output specific dissipation rate boundary condition
    omega.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, wall_functions, case_name, version)

    # output nu tilda boundary conditions
    nuTilda.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, wall_functions, case_name, version)

    # output turbulent viscosity boundary condition
    nut.write_boundary_condition(BC, outlet_type, inlet_velocity, TKE_intensity, reference_length, case_name, version)

def create_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)
    if not os.path.exists(os.path.join(name, '0')):
        os.makedirs(os.path.join(name, '0'))


if __name__ == '__main__':
    main()