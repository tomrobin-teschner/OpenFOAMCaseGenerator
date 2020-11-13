def dirichlet(file_id, initial_field):
    file_id.write('        type            fixedValue;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def neumann(file_id):
    file_id.write('        type            zeroGradient;\n')


def no_slip_wall(file_id):
    file_id.write('        type            noSlip;\n')


def advective(file_id):
    file_id.write('        type            advective;\n')
    file_id.write('        phi             phi;\n')


def inlet_outlet(file_id, internal_field):
    file_id.write('        type            inletOutlet;\n')
    file_id.write('        inletValue      ' + internal_field + ';\n')


def periodic(file_id):
    file_id.write('        type            cyclic;\n')


def empty(file_id):
    file_id.write('        type            empty;\n')


def kqRWallFunction(file_id, internal_field):
    file_id.write('        type            kqRWallFunction;\n')
    file_id.write('        value           ' + internal_field + ';\n')


def epsilonWallFunction(file_id, internal_field):
    file_id.write('        type            epsilonWallFunction;\n')
    file_id.write('        value           ' + internal_field + ';\n')


def omegaWallFunction(file_id, internal_field):
    file_id.write('        type            omegaWallFunction;\n')
    file_id.write('        value           ' + internal_field + ';\n')


def nutUSpaldingWallFunction(file_id):
    file_id.write('        type            nutUSpaldingWallFunction;\n')
    file_id.write('        value           uniform 0;\n')


def zeroCalculated(file_id):
    file_id.write('        type            calculated;\n')
    file_id.write('        value           uniform 0;\n')