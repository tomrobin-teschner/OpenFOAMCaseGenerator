How to use the OpenFOAM case generator
======================================

This section will show you how to use the OpenFOAMCaseGenerator. The quick start section will help you get to grips with the basic usage of the case generator, while the design philosophy section will give you an overview of the design choices that were made when developing the case generator, which include how policies drive the case setup and how it can be extended with custom c++ code. Finally, the protection against common mistakes section will show you how the case generator will help you avoid common pitfalls when setting up a case.

Quick Start
-----------

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

Design philosophy
-----------------

Whenever you have to setup a new case in OpenFOAM, you are required to provide detailed inputs across various files. This is error prone and as mentioned in the :doc:`Motivation<motivation>`, usually results in tutorial cases being copied and modified to best represent the case that should be solved. This commonly results in some parameters being not set correctly which are left to the value used in the underlying tutorial case, and thus this approach can lead to incorrect case setups, where the user is not necessarily aware that something went wrong, only later when looking at the results. 

To circumvent this issue, the OpenFOAMCaseGenerator only requires you to fill in your intend in logical separated sections within a single input file. If you don't need certain sections, you can ignore them but be assured that no unnecessary files or wrong inputs will be generated.

Within the ``input/cases`` directory, there are a number of example cases which you can use as a starting point for your own case. Each case has its own input file which is specific to that case. The input file is a python class which inherits from a base class (more on that in the :doc:`Creating custom cases <custom_cases>`) in which you have a dictionary defined that contains a few subsections. Each subsection is defined below and a short summary of the input you can provide is given below:

file_properties
***************

Specify the case name and where the generated case should be written to. It also deals with how the mesh file is handled and either copies a ``polyMesh`` directory into the ``constant`` directory of the case setup or a corresponding ``blockMeshDict`` and/or a ``snappyHexMeshDict`` into the ``system`` directory.

parallel_properties
*******************

Specify if the case should be run in parallel and if so, how many processor should be used. This influences the set up of the ``decomposeParDict``, which is used to handle the domain decomposition task. Furthermore, the ``Allrun`` script will receive the correct ``MPI`` command to run the application in parallel with the right number of processors, along with the right command to reconstruct the case back into one once the simulation is finished.

boundary_properties
*******************

Here we specify the boundary conditions of the case along with some boundary specific setup. We can, for example, specify if we want to use a custom boundary inlet profile (in which case we need to specify the path to the c++ code which to use as the custom boundary condition). Furthermore, we can setup all settings related to the DFSEM inlet boundary condition (useful for LES simulations with open boundaries), however, the use is discouraged as the implementation seems buggy and not fixed yet. **IMPORTANT:** When generating the mesh (blockMesh, snappyHexMesh, external tool), make sure that wall patches have the type WALL, empty patches the type EMPTY and **EVERYTHING ELSE** is set to patch (i.e. even symmetry patches should be set to patch). If this is not done you may encounter errors when running OpenFOAM.

flow_properties
***************

This is where we set the flow properties of the fluid such as the velocity, pressure, viscosity, temperature and density at open (inlet) boundaries. We can either specify these dimensional units, or, use non-dimensional quantities such as the Reynolds and Mach number to steer the simulation setup. Depending on which setting is set (i.e. dimensional or non-dimensional quantities), the other set that is not specified will be computed from the provided input. In addition, this place also handles the initial conditions and we are able to use custom initial conditions where we need to, again, specify the location of the c++ script that shoulod be used for the custom initial conditions.

solver_properties
*****************

This entry handles all input around the solver that needs to be used, along with information on when to start and for how long to run it. Under-relaxation is also specified here which essential determines the convergence rate of the solver (or divergence if set too high).

spatial_discretisation
**********************

Here we can only make a few choices, whether the case is steady or unsteady, whether to use first-order for turbulent quantities when solving RANS models and, most important of all, which discretisation policy to use. Here we essential steer the behaviour of our flow and we can choose between a default, robust, accurate and total-variation diminishing (tvd) approach. This will set sensible default values which can be fine tuned if required by the case.

turbulence_properties
*********************

This sub-dictionary specifies the turbulence model that should be used. For RANS simulations, all OpenFOAM supported models can be chosen (i.e. those based on linear and non-linear eddy viscosity models, transitional model, Reynolds stresses-based models as well as scale adaptive-based models). When using RANS, calculating initial conditions for all boundary files can be a daunting task. Each variable needs to be specified for each boundary condition which adds a minimum of two files (variables) to the zero directory for which initial and boundary conditions can be specified. Commercial solvers like ANSYS Fluent take responsibility away here from the user by asking them to provide engineering properties that can be easily accessed or at least reasoned about (e.g. the freestream turbulence intensity). The same approach is taken here and a further simplification over ANSYS Fluent, for example, is taken, in that the wall modelling approach does not need to be explicitly defined but rather the intention should be stated, i.e. if the wall should be resolved (the y+ value should be one or less, here indicated as a low Reynolds number modelling approach) or if wall functions should be used (the y+ value should be within the log layer, i.e. greater than 30, here indicated as a high Reynolds number modelling approach). Along with this, the type of flow needs to be prescribed (internal or external) from which the turbulent length scale is calculated, together with the freestream turbulence intensity and characteristic length. If the flow can not be classified as such, the turbulent to laminar ratio can be prescribed instead or left to be calculated on the freestream turbulence intensity entirely if such a statement can not be made. In addition to RANS, full support for LES and DES (DDES, IDDES) simulations are supported and the user can choose these here as well with all required options.

convergence_control
*******************

Here we control the overall convergence behaviour of the simulation. In total there are three parts to this. First, we can specify an overall convergence parameter which is used to check if the simulation has converged to a prescribed threshold (typically used for steady state simulations). Then we also need to specify the convergence threshold for all inner iterations (which will be used to judge convergence for each iteration for all implicit matrix solvers). These will not influence if the simulation should be stopped but rather steer only the inner (not outer) iterations. Finally, we can prescribe a convergence parameter based on integral quantities (such as the lift or drag coefficient) and we can choose an arbitrary number of force coefficients to monitor simultaneously (for example, it is common to use both lift and drag to judge convergence). If these do not change within a user-specified averaging window below a certain convergence threshold, the simulation is deemed converged (and stopped), even if the solver itself has not converged to a user specified convergence criterion.

dimensionless_coefficients
**************************

Here we can specify if we want to calculate non-dimensional force coefficients, as well as pressure coefficients and wall shear stresses (which can, in turn, be used to calculate the skin friction coefficient). All required input is done here, expect for the lift, drag and pitch axis, which is calculated from the **flow_properties** inputs, where we have to specify the **axis_aligned_flow_direction**. Based on this input, the lift, drag and pitch axis can be uniquely identified. The setup of the **dimensionless_coefficients** is required if these should be used to judge convergence, as specified in the **convergence_control** dictionary.

additional_fields
*****************

This entry allows us to write out additional quantities during the calculation. For compressible flows, the Mach number is automatically set up so no additional change is required here. Currently,Vorticity, Enstrophy, the Q and Lambda2-criterion are supported. The additional field(s) that should be written out are specified as a list and more than one additional field can be written out. You can specify an additional field here and use it later (in the iso surfaces, for example) to create a plot using the variable specified here, i.e. the order of setup is important for OpenFOAM (the additional fields need to be specified before) which is automatically taken care of here.

point_probes
************

This presents the possibility to prescribe points in the flow field to monitor specific quantities. This may be useful if certain locations in a domain have experimental data available for which comparions can be made. Additionally, for scale resolved turbuent simulations we can use these point probes as inputs for energy sepctra calculations.

line_probes
***********

Just like the point probes, this utility allows us to monitor a quantity along a prescribed line, useful for generating profiles for monitored quantities.

cutting_planes
**************

Cutting planes are useful for larger simulations where we know in advanced which planes we want to examine. For RANS simulations, this may not necessarily be an advantage (as we only get one timestep, i.e. the steady state solution), for any unsteady simulations, however, especially scale resolved 3D simulations, we can use this cutting plane feature to extract only 2D planes at locations of interest which we can then use for either further time-dependent post processing or to generate an animation of the flow. The files will be written out to the post-processing directory and are, by default, rather inaccessible (each plane needs to be loaded separately). To automate that process, each time a cutting plane is requested, a python utility script is also copied into the case setup which will generate a master VTP file which contains all the locations of the individual planes. We only need to load this VTP file in paraview which will give us access to all the individual cutting planes. This utility script is also added to the ``Allrun`` script so that the user does not need to do anything extra, this is all handled automatically.

iso_surfaces
************

ISO surfaces are useful for 3D simulations to monitor the flow of a specific quantity. A classical example is that of ISO surfaces of the Q-criterion. Traditionally, we would need to store all 3D solutions for the duration for which the iso surfaces should be monitored (and perhaps be used for generating an animation). This can quickly escalate and results in a rather large storage requirement. To circumvent this, we can specify here ISO contours we would like to write out during the simulation along with additional fields on these ISO surfaces so that we can colour them accordingly during post processing. This reduces the computational storage requirement significantly and we can store longer periods of time during which we would like to observe a quantity. The setup is done in such a way that we can specify a number of variables for which we would like to write out ISO surfaces. However, we can also specify the same variable several times if we want to observe only one variable but with different ISO values (for example, if the exact ISO value can not be fully reasoned about beforehand). Similar to the cutting planes described above, the ISO surfaces are written out in an inaccessible format (requiring all surfaces to be loaded individually). Thus, the same utility script, which is also used for the cutting planes, is copied into the case setup and used to generate a global VTP file which can then easily load all required surfaces into paraview.

post_processing
***************

OpenFOAM offers a range of post-processing function objects. On top of that, there may be certain user-defined post-processing scripts that we may want to run once the simulation is done. The post_processing dictionary allows for exactly that. We can write all function objects in one file and then point to it within the function_objects dictionary. Similarily, we can also copy custom made python scripts to the case setup along with additional files that are required by the python script. For example, we may wish to compare experimental results with our OpenFOAM solution, in this case we may wish to copy experimental data, stored within text files, into our case setup along with the python script. All python scripts will be added to the Allrun file so that post-processing is done automatically after the simulation is done.

Policy-driven case setups
-------------------------

One central point of the OpenFOAMCaseGenerator is that inputs are, where possible, driven by policies, rather than explicit user-input. For example, instead of asking the user to make choices about which discretisation scheme to use for the divergence and gradient operator for all the different variables, the user has to provide their intent rather than explicit inputs. For example, there are four different discretisation policies available:

* default
* accuracy
* robustness
* tvd

Each choice signals the intent of the user, for example, ``default`` will likely work for a range of applications and, if no other information is available, it is probably a good starting point. This will give a second-order discretisation with just enough numerical dissipation to handle moderate mesh quality. If the mesh quality get's too bad or strong discontinuities are present in the flow, then ``robustness`` or ``tvd`` may be a better choice, while ``accuracy`` is intended for scale-resolved turbulence simulations, such as DNS, LES and DES simulations.

There are other choices available as well, most notably the RANS turbulence model discretisation policy, where we specify if we want to use a boundary layer resolved grid (i.e. a y+ value of 1 or less) or a boundary layer modelled grid (i.e. a y+ value of 30 or larger). This will then influence how the boundary conditions will be set up and if wall functions are to be used based on the turbulence model selected, if that RANS turbulence model supports wall functions.

Custom C++ code injection
-------------------------

The OpenFOAMCaseGenerator also supports to directly inject C++ code into the case setup. This is useful in situations where we need either custom boundary or initial conditions and where we don;t want to provide our own custom developed boundary condition class. Support is also provided for custom post-processing routines and in this way the user just has to focu on writing the c++ code, all the rest in terms of boiler-plate code around the c++ code is handled by the OpenFOAMCaseGenerator. The ``Taylor Green Vortex`` problem shows how to use custom C++ code as part of their initial conditions.


Protection against common mistakes
----------------------------------

It is easy to set up a simulation which provides a perfectly acceptable case setup and which will run in OpenFOAM which is, however, non-physical or is deemed to give inaccurate results. For this, a case checking utility is implemented which will prevent the user from setting up the case with wrong settings. For example, there is no point to say we want to perform an LES simulation with a steady state solver, or, specify the flow to be compressible but then requesting an incompressible solver. These checks are implemented to help the user avoid common pitfalls and, depending on the severity of the situation, either a warning or error (which will then abort the case setup) will be issued. This is similar to the ANSYS Fluent check case but more pertinent to OpenFOAM specific settings.