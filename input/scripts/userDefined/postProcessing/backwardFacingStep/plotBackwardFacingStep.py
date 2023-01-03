import os
import numpy as np
import matplotlib.pyplot as plt


def main():
    experimental_data = get_experimental_data()
    numerical_data = get_numerical_data()

    print('>>> Plotting skin friction coefficient')
    plot_skin_friction_profile(numerical_data, experimental_data)
    print('>>> Plotting inlet velocity profile')
    plot_inlet_velocity_profile(numerical_data, experimental_data)
    print('>>> Plotting velocity profiles')
    plot_velocity_profiles(numerical_data, experimental_data)
    print('>>> Calculating reattachment point')
    calculate_reattachment_point(numerical_data)


def calculate_reattachment_point(numerical_data):
    x    = numerical_data[5][:].transpose()[0]
    tauw = numerical_data[5][:].transpose()[6]

    for i in range(1, len(numerical_data[5][:].transpose()[0])):
        product = tauw[i-1] * tauw[i]
        if product < 0:
            magtau = abs(tauw[i-1]) + abs(tauw[i])
            dist = abs(tauw[i-1]) / magtau
            dx = x[i] - x[i-1]
            reattachment_point = x[i] + dx * dist
            if reattachment_point > 5 and reattachment_point < 7.5:
                error = 100 * abs(reattachment_point - 6.26) / 6.26
                print(f'    Reattachment in experiment: 6.26+-0.1')
                print(f'    Reattachment in OpenFOAM  : {reattachment_point:4.2f}')
                print(f'    Relative error            : {error:4.2f}%')


def get_experimental_data():
    x_by_H_m4_path = os.path.join('postProcessing', 'x_by_H=-4.csv')
    x_by_H_1_path = os.path.join('postProcessing', 'x_by_H=1.csv')
    x_by_H_4_path = os.path.join('postProcessing', 'x_by_H=4.csv')
    x_by_H_6_path = os.path.join('postProcessing', 'x_by_H=6.csv')
    x_by_H_10_path = os.path.join('postProcessing', 'x_by_H=10.csv')
    cf_path = os.path.join('postProcessing', 'experimental_cf_data.csv')

    x_by_H_m4 = np.genfromtxt(x_by_H_m4_path, delimiter=',')
    x_by_H_1 = np.genfromtxt(x_by_H_1_path, delimiter=',')
    x_by_H_4 = np.genfromtxt(x_by_H_4_path, delimiter=',')
    x_by_H_6 = np.genfromtxt(x_by_H_6_path, delimiter=',')
    x_by_H_10 = np.genfromtxt(x_by_H_10_path, delimiter=',')
    cf = np.genfromtxt(cf_path, delimiter=',')

    return [x_by_H_m4, x_by_H_1, x_by_H_4, x_by_H_6, x_by_H_10, cf]


def get_numerical_data():
    # get last time directory in first solution directory (should be the same for all directories)
    solution_path = os.path.join('postProcessing', 'x_by_H=-4')
    solution_directories = os.listdir(solution_path)
    final_solution = solution_directories[-1]

    x_by_H_m4_path = os.path.join('postProcessing', 'x_by_H=-4', final_solution, 'x_by_H=-4_U_wallShearStress.xy')
    x_by_H_1_path = os.path.join('postProcessing', 'x_by_H=1', final_solution, 'x_by_H=1_U_wallShearStress.xy')
    x_by_H_4_path = os.path.join('postProcessing', 'x_by_H=4', final_solution, 'x_by_H=4_U_wallShearStress.xy')
    x_by_H_6_path = os.path.join('postProcessing', 'x_by_H=6', final_solution, 'x_by_H=6_U_wallShearStress.xy')
    x_by_H_10_path = os.path.join('postProcessing', 'x_by_H=10', final_solution, 'x_by_H=10_U_wallShearStress.xy')
    cf_path = os.path.join('postProcessing', 'bottom_wall', final_solution, 'bottom_wall_U_wallShearStress.xy')

    x_by_H_m4 = np.genfromtxt(x_by_H_m4_path, delimiter='\t')
    x_by_H_1 = np.genfromtxt(x_by_H_1_path, delimiter='\t')
    x_by_H_4 = np.genfromtxt(x_by_H_4_path, delimiter='\t')
    x_by_H_6 = np.genfromtxt(x_by_H_6_path, delimiter='\t')
    x_by_H_10 = np.genfromtxt(x_by_H_10_path, delimiter='\t')
    cf = np.genfromtxt(cf_path, delimiter='\t')

    # print(x_by_H_m4[:].transpose()[2])
    return [x_by_H_m4, x_by_H_1, x_by_H_4, x_by_H_6, x_by_H_10, cf]
    

def plot_skin_friction_profile(numerical_data, experimental_data):
    fig, ax = plt.subplots()
    ax.plot(experimental_data[5].transpose()[0][:], experimental_data[5].transpose()[1][:],
            marker='s', markersize=8, markerfacecolor='None', markeredgecolor='r', linestyle='None')
    ax.plot(numerical_data[5][:].transpose()[0], -1.0 * numerical_data[5][:].transpose()[6] / 6.48, '-r')

    ax.set(xlabel='x/H', ylabel='Cf')
    ax.grid()
    plt.xlim([0, 30])
    plt.ylim([-0.002, 0.004])

    fig.savefig('postProcessing/skin_friction_profile.png', dpi=600, facecolor='w', edgecolor='w',
                orientation='portrait', format=None, transparent=False, bbox_inches='tight', pad_inches=0.1,
                metadata=None)
    plt.close('all')


def plot_inlet_velocity_profile(numerical_data, experimental_data):
    fig, ax = plt.subplots()
    ax.plot(experimental_data[0].transpose()[1][:], experimental_data[0].transpose()[0][:],
            marker='s', markersize=8, markerfacecolor='None', markeredgecolor='r', linestyle='None')
    ax.plot(numerical_data[0][:].transpose()[3] / 3.6, numerical_data[0][:].transpose()[2], '-r')

    ax.legend(['x/H=-4 (exp)', 'x/H=-4 (cfd)'], loc='upper left')
    ax.set(xlabel='U/Uref', ylabel='y/H')
    ax.grid()
    plt.xlim([0, 1.05])
    plt.ylim([1, 5])

    fig.savefig('postProcessing/inlet_velocity_profile.png', dpi=600, facecolor='w', edgecolor='w',
                orientation='portrait', format=None, transparent=False, bbox_inches='tight', pad_inches=0.1,
                metadata=None)
    plt.close('all')


def plot_velocity_profiles(numerical_data, experimental_data):  
    fig, ax = plt.subplots()
    ax.plot(experimental_data[1].transpose()[1][:], experimental_data[1].transpose()[0][:],
            marker='s', markersize=8, markerfacecolor='None', markeredgecolor='r', linestyle='None')
    ax.plot(numerical_data[1][:].transpose()[3] / 3.6, numerical_data[1][:].transpose()[2], '-r')
    ax.plot(experimental_data[2].transpose()[1][:], experimental_data[2].transpose()[0][:],
            marker='^', markersize=8, markerfacecolor='None', markeredgecolor='b', linestyle='None')
    ax.plot(numerical_data[2][:].transpose()[3] / 3.6, numerical_data[2][:].transpose()[2], '-b')
    ax.plot(experimental_data[3].transpose()[1][:], experimental_data[3].transpose()[0][:],
            marker='v', markersize=8, markerfacecolor='None', markeredgecolor='g', linestyle='None')
    ax.plot(numerical_data[3][:].transpose()[3] / 3.6, numerical_data[3][:].transpose()[2], '-g')
    ax.plot(experimental_data[4].transpose()[1][:], experimental_data[4].transpose()[0][:],
            marker='>', markersize=8, markerfacecolor='None', markeredgecolor='k', linestyle='None')
    ax.plot(numerical_data[4][:].transpose()[3] / 3.6, numerical_data[4][:].transpose()[2], '-k')
    
    ax.legend(['x/H=1 (exp)', 'x/H=1 (cfd)', 'x/H=4 (exp)', 'x/H=4 (cfd)', 'x/H=6 (exp)', 'x/H=6 (cfd)', 'x/H=10 (exp)',
               'x/H=10 (cfd)'], loc='upper left')
    ax.set(xlabel='U/Uref', ylabel='y/H')
    ax.grid()
    plt.xlim([-0.4, 1.2])
    plt.ylim([0, 3])

    fig.savefig('postProcessing/velocity_profiles.png', dpi=600, facecolor='w', edgecolor='w', orientation='portrait',
                format=None, transparent=False, bbox_inches='tight', pad_inches=0.1, metadata=None)
    plt.close('all')


if __name__ == '__main__':
    main()