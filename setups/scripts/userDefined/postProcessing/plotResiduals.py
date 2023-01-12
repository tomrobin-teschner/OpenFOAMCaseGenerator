import os
import matplotlib.pyplot as plt


def main():
    print('>>> Plotting residuals')
    # get residual files
    dirs = os.listdir(os.path.join('postProcessing', 'residuals'))
    for dir in dirs:
        # read residuals
        res_file = open(os.path.join('postProcessing', 'residuals', dir, 'solverInfo.dat'), 'r')
        lines = res_file.readlines()

        # get all variables that needs to be plotted
        header = lines[1].strip().split()
        index = 0
        var_index = []
        for var in header:
            if var.find('_initial') != -1:
                var_index.append(index)
            index += 1

        # store variable name
        var_name = []
        for index in var_index:
            var_name.append(header[index][:-8])

        # get residuals for each variable, offset by -1 to account for additional entry in header
        res = []
        time = []
        for var in var_name:
            res.append([])

        for i in range(2, len(lines)):
            line = lines[i].strip().split()
            time.append(float(line[0]))
            index = 0
            for var in var_index:
                res[index].append(float(line[var-1]))
                index += 1

        # plot residuals
        fig, ax = plt.subplots()
        for var_res in res:
            ax.plot(time, var_res)

        ax.legend(var_name, loc='upper right')
        ax.set(xlabel='iterations', ylabel='residuals')
        ax.set_yscale('log')
        ax.grid()

        fig.savefig('postProcessing/residuals_' + dir + '.png', dpi=600, facecolor='w', edgecolor='w', orientation='portrait',
                    format=None, transparent=False, bbox_inches='tight', pad_inches=0.1, metadata=None)

        plt.close('all')


if __name__ == '__main__':
    main()
