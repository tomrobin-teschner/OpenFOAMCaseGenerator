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


def kqRWallFunction(file_id, initial_field):
    file_id.write('        type            kqRWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def epsilonWallFunction(file_id, initial_field):
    file_id.write('        type            epsilonWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def omegaWallFunction(file_id, initial_field):
    file_id.write('        type            omegaWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def nutkWallFunction(file_id, initial_field):
    file_id.write('        type            nutkWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def kLowReWallFunction(file_id, initial_field):
    file_id.write('        type            kLowReWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def epsilonLowReWallFunction(file_id, initial_field):
    file_id.write('        type            epsilonLowReWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def nutLowReWallFunction(file_id, initial_field):
    file_id.write('        type            nutLowReWallFunction;\n')
    file_id.write('        value           ' + initial_field + ';\n')


def zeroCalculated(file_id):
    file_id.write('        type            calculated;\n')
    file_id.write('        value           uniform 0;\n')