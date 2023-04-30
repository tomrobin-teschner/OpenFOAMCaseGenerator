Usage
=====

The root folder has one file, the ``OpenFOAMCaseGenerator.py`` script. It requires one additional command line argument: ``--case=case_name``. This tells the case generator which case setup to generate. The input file is specific for each case and example case setups can be found in the ``input/cases`` directory. So, to generate the case for the Naca0012 airfoil, run the following command 

``python3 OpenFOAMCaseGenerator.py --case=Naca0012``

You can also list all available case setups directly on the command line using

``python3 OpenFOAMCaseGenerator.py --list-cases``

This will show all available case setups in the ``input/cases`` folder and may be more convenient to use.

Each case comes with a few parameters that are case specific and that we can fine-tune. For example, if we run the Naca0012 aerofoil example, we will see the following output

.. code-block:: markdown

    Application    : OpenFOAMCaseGenerator
    Source         : https://github.com/tomrobin-teschner/OpenFOAMCaseGenerator
    Copyright      : Tom-Robin Teschner, 2020-[current year]
    License        : MIT
    Version        : [current version]

    Generated case : Naca0012
    Using input    : input/cases/Naca0012/Naca0012.py

    Case parameters
    - run_in_parallel      : False
    - number_of_processors : 1
    - reynolds_number      : 6000000
    - angle_of_attack      : 0
    - rans_model           : RansModel.kOmegaSST
    - mesh                 : coarse

We can see at the bottom that we can fine-tune parameters that make sense for this case, such as the angle of attack and the reynolds number. If we wanted to change any of these, we simply tun the case generator again and pass either the ``--parameter:key=value`` or ``-p:key=value`` construct, where the ``key`` is the name listed in the parameter list (for example, ``reynolds_number``) and the ``value`` is the value we want to set this parameter to. If we wanted to change the angle of attack to 10 degrees, for example, we would invoke the case generator as

``python3 OpenFOAMCaseGenerator.py --case=Naca0012 --parameter:angle_of_attack=10``

or

``python3 OpenFOAMCaseGenerator.py --case=Naca0012 -p:angle_of_attack=10``

We will see in the next section, how we can define our own parameters, as well as how to setup new cases from scratch. If you want your case to be included in future distributions of this software, please open a pull request at ``https://github.com/tomrobin-teschner/OpenFOAMCaseGenerator``.

Protection against common mistakes
----------------------------------

It is easy to set up a simulation which provides a perfectly acceptable case setup and which will run in OpenFOAM which is, however, non-physical or is deemed to give inaccurate results. For this, a case checking utility is implemented which will prevent the user from setting up the case with wrong settings. For example, there is no point to say we want to perform an LES simulation with a steady state solver, or, specify the flow to be compressible but then requesting an incompressible solver. These checks are implemented to help the user avoid common pitfalls and, depending on the severity of the situation, either a warning or error (which will then abort the case setup) will be issued. This is similar to the ANSYS Fluent check case but more pertinent to OpenFOAM specific settings.