import sys, os


def main():
    print('>>> Writing VTP loader for', str(sys.argv[1:]))
    # get plane names from command line arguments
    assert len(sys.argv) > 1, 'Need at least one plane to process'
    for i in range(1, len(sys.argv)):
        name = sys.argv[i]
        sub_dirs = os.listdir(os.path.join('postProcessing', name))
        file_id = open(os.path.join('postProcessing', name + '.pvd'), 'w')
        file_id.write('<?xml version="1.0"?>\n')
        file_id.write('<VTKFile type="Collection">\n')
        file_id.write('  <Collection>\n')
        for dir in sub_dirs:
            file_id.write('    <DataSet timestep="' + str(dir) + '" ')
            file_id.write('part="0" ')
            file_id.write('file="' + str(os.path.join(name, str(dir), str(name + '.vtp"/>'))) + '\n')
        file_id.write('  </Collection>\n')
        file_id.write('</VTKFile>\n')


if __name__ == '__main__':
    main()