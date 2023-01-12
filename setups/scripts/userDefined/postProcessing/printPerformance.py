import os


def main():
    print('>>> Printing performance')
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
            if var.find('_iters') != -1:
                var_index.append(index)
            index += 1

        # store variable name
        var_name = []
        for index in var_index:
            var_name.append(header[index][:-6])

        # get residuals for each variable, offset by -1 to account for additional entry in header
        iterations = []
        time = []
        for var in var_name:
            iterations.append([])

        for i in range(2, len(lines)):
            line = lines[i].strip().split()
            time.append(float(line[0]))
            index = 0
            for var in var_index:
                iterations[index].append(float(line[var-1]))
                index += 1

        # print performance to screen
        print('--- performance ---')
        for index in range(0, len(var_name)):
            average = sum(iterations[index]) / len(iterations[index])
            print(f"Average iterations of, {var_name[index]}, : {average:.1f}")

if __name__ == '__main__':
    main()
