import subprocess
import os
import shutil


def test_all():
    test_path = os.path.join('tests', 'cases')
    create_test_directory(test_path)

    # run all tests here
    test_naca_0012(test_path)
    test_taylor_green_vortex(test_path)
    test_wing_and_winglet(test_path)

    # clean up after ourselves
    tear_down_test_directory(test_path)


def create_test_directory(test_path):
    if not os.path.exists(test_path):
        os.makedirs(test_path)


def tear_down_test_directory(test_path):
    shutil.rmtree(test_path)


def test_naca_0012(test_path):
    run_directory = '--replace=file_properties/run_directory:' + test_path

    print('Testing --input=naca_0012 ........................................................................ ', end='')
    base_test = ['python', 'OpenFOAMCaseGenerator.py', '--input=naca_0012', run_directory]
    subprocess.run(base_test, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('DONE')

    print('Testing --input=naca_0012 --replace=flow_properties/flow_type:0 .................................. ', end='')
    modified_test_1 = base_test + ['--replace=flow_properties/flow_type:0']
    subprocess.run(modified_test_1, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('DONE')


def test_taylor_green_vortex(test_path):
    run_directory = '--replace=file_properties/run_directory:' + test_path

    print('Testing --input=taylor_green_vortex .............................................................. ', end='')
    base_test = ['python', 'OpenFOAMCaseGenerator.py', '--input=taylor_green_vortex', run_directory]
    subprocess.run(base_test, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('DONE')


def test_wing_and_winglet(test_path):
    run_directory = '--replace=file_properties/run_directory:' + test_path

    print('Testing --input=wing_and_winglet ................................................................. ', end='')
    base_test = ['python', 'OpenFOAMCaseGenerator.py', '--input=wing_and_winglet', run_directory]
    subprocess.run(base_test, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('DONE')


if __name__ == '__main__':
    test_all()
