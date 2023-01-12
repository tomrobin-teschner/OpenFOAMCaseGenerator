import os
import numpy as np
import matplotlib.pyplot as plt

TIME = 0
EKIN = 1
DISS = 2 

def main():
    ref_solution = get_reference_solution()
    num_solution = get_numerical_solution()

    plot_kinetic_energy(ref_solution, num_solution)
    plot_dissipation_of_kinetic_energy(ref_solution, num_solution)  


def plot_kinetic_energy(ref_solution, num_solution):
    fig, ax = plt.subplots()
    ax.plot(num_solution[TIME][:], num_solution[EKIN][:])
    ax.plot(ref_solution[TIME][:], ref_solution[EKIN][:])
    ax.legend(['OpenFOAM', 'spectral, 512^3'], loc='upper right')
    ax.set(xlabel='time [s]', ylabel='E_kin')
    ax.grid()

    fig.savefig('postProcessing/tgv_e_kin_.png', dpi=600, facecolor='w', edgecolor='w', orientation='portrait',
                format=None, transparent=False, bbox_inches='tight', pad_inches=0.1, metadata=None)
    plt.close('all')


def plot_dissipation_of_kinetic_energy(ref_solution, num_solution):
    fig, ax = plt.subplots()
    ax.plot(num_solution[TIME][:], num_solution[DISS][:])
    ax.plot(ref_solution[TIME][:], ref_solution[DISS][:])

    ax.legend(['OpenFOAM', 'spectral, 512^3'], loc='upper right')
    ax.set(xlabel='time [s]', ylabel='E_kin')
    ax.grid()

    fig.savefig('postProcessing/tgv_dissipation_of_e_kin_.png', dpi=600, facecolor='w', edgecolor='w',
                orientation='portrait', format=None, transparent=False, bbox_inches='tight', pad_inches=0.1,
                metadata=None)
    plt.close('all')


def get_reference_solution():
    path_to_ref_soluition = os.path.join('postProcessing', 'taylor_green_vortex_512_ref.dat')
    num_line_headers = get_number_of_lines_of_header(path_to_ref_soluition)
    num_lines = get_number_of_lines_in_file(path_to_ref_soluition)

    zero_vec = np.zeros(num_lines - num_line_headers)
    ref_solution = np.array([zero_vec, zero_vec, zero_vec])

    with open(path_to_ref_soluition, 'r') as tgv_ref:
        counter = 0
        for line in tgv_ref:
            # ignore header
            if counter >= num_line_headers:
                data = line.strip().split()
                ref_solution[TIME][counter - num_line_headers] = float(data[TIME])
                ref_solution[EKIN][counter - num_line_headers] = float(data[EKIN])
                ref_solution[DISS][counter - num_line_headers] = float(data[DISS])
            counter += 1
    return ref_solution


def get_numerical_solution():
    path_to_numeric_soluition = os.path.join('postProcessing', 'volIntK', '0', 'volFieldValue.dat')
    num_line_headers = get_number_of_lines_of_header(path_to_numeric_soluition)
    num_lines = get_number_of_lines_in_file(path_to_numeric_soluition)

    zero_vec = np.zeros(num_lines - num_line_headers)
    numerical_solution = np.array([zero_vec, zero_vec, zero_vec])

    with open(path_to_numeric_soluition, 'r') as tgv_ref:
        counter = 0
        for line in tgv_ref:
            # ignore header
            if counter >= num_line_headers:
                data = line.strip().split()
                numerical_solution[TIME][counter - num_line_headers] = float(data[TIME])
                numerical_solution[EKIN][counter - num_line_headers] = float(data[EKIN])
            counter += 1
    
    # calculate dissipation rate of kinetic energy
    for i in range (1, num_lines - num_line_headers):
        ek1 = numerical_solution[EKIN][i]
        ek0 = numerical_solution[EKIN][i-1]
        t1 = numerical_solution[TIME][i]
        t0 = numerical_solution[TIME][i-1]
        dekin = ek1 - ek0
        dt = t1 - t0
        numerical_solution[DISS][i] = - dekin / dt
    numerical_solution[DISS][0] = numerical_solution[DISS][1]
    return numerical_solution


def get_number_of_lines_in_file(path):
    return sum(1 for line in open(path, 'r'))


def get_number_of_lines_of_header(path):
    with open(path, 'r') as f:
        counter = 0
        for line in f:
            if line.strip()[0] != "#":
                return counter
            counter += 1


if __name__ == '__main__':
    main()
