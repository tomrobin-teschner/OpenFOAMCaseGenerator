[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Generic badge](https://img.shields.io/badge/Version-v2.0.0-red.svg)](https://shields.io/)

> :warning: This is a pre-release, version 2.0.0-alpha.12. This documentation may be outdated and will be revised for the release candidate version 2.0.0. Work in progress. The interface may change, proceed with caution.

## Motivation

OpenFOAM has become the de-facto standard Computational Fluid Dynamics (CFD) solver of choice among open-source projects. It offers a rich set of feature and can easily compete with other commercial solvers. In-fact, for most applications, it offers probably more features than can be found in any other CFD solver of similar nature (i.e. general purpose CFD solvers).

To set up a problem in OpenFOAM requires experience, patience and a good collection of resources for consultation. Perhaps the biggest help here are the tutorial cases that come with the default distribution of OpenFOAM. It is common to copy and paste a tutorial case and then adjust it for one's own flow problem. There is in-fact a dedicated utility script ```foamCloneCase``` which can help with this. Using this approach, however, should be regarded as a rather poor practice and in-fact is exactly going against the DRY (Don't repeat yourself) principle in programming terms, where copy and pasting of source code is discouraged as it is difficult to maintain and a potential source of errors (bugs). In-fact, this copy and pasting approach where tutorial cases are adapted for another problem has shown to be error prone and yielding to a lot of wrong results.

On the other hand, this approach is still better than writing a case setup from scratch, which is done in an almost domain specific language (DSL) based on c++. The syntax is difficult to look up, at times, due to a lack of a well written documentation for advanced features (basic features are reasonably well documented) and also difficult to memorise. Thus, copy and pasting of tutorial files becomes an attractive and appealing approach.

This application, the OpenFOAMCaseGenerator, aims to get rid of the copy and pasting approach by producing reproducible case setups that generate all required files to run a case (along with an OpenFOAM-like Allrun bash script to execute all required steps, i.e. pre-processing, solving and post-processing). The case setups are reproducible as their settings can be written out to a json file which can then be later used as input to the case generator to setup the same case again.

The idea is very much inspired by build tools such as CMake or Meson, which act as a meta build system for compiled languages such as c/c++ or Fortran. Just as CMake, Meson (or similar meta build systems) produce the actual build script (such as Make or Ninja files) which are then used to perform the actual build, the OpenFOAMCaseGenerator does not interact with OpenFOAM itself but rather perform all required steps to setup a case which can then be used by OpenFOAM, completely eliminating the need to copy and paste tutorial cases from elsewhere.

Thiss is not all, however. OpenFOAM does not make any assumptions about any case and thus requires a lot of boilerplate setup. This offers a really good opportunity to fine tune a specific case but also requires expert knowledge when it comes to setting up a case. Instead of asking for all of these inputs, this case generator offers specific policies instead, which are then used to drive the case setup. For example, instead of providing all required numerical discretisation schemes, the user may choose among several policies (default, robust, accuracy or total-variation diminishing (TVD)). This is a much clearer intend and does not require knowledge about all numerical discretisation schemes. These can still be later modified if needed but a sensible default setup can be achieved in this manner. Another important aspect of the case setup are the boundary conditions, especially for turbulent flow calculations. Here, again, the user expresses only the intent (i.e should walls be resolved or modelled through wall functions, for example, using RANS) and the type of flow (internal or external flow) and the rest of the intitial and boundary conditions are calculated accordingly.

OpenFOAM also offers the ability to inject c++ code directly into the initial and boundary conditions. This can be considered an advanced feature for which little documentation can be found. This case generator, again, provides all the boilerplate code that is required and the user only needs to provide the actual c++ code which will be then inserted in the right place. Example code is also provided along with this case generator which can be used to understand how to query OpenFOAM for domain specific variables such as the coordinate arrays or current timestep.

In short, the OpenFOAMCaseGenerator takes all the heavy lifting from the user and provides a reproducible case setup with sensible default options that can be used to setup cases for one's own calculations.

## Usage

### Running the Case Generator

The root folder has one file, the ```OpenFOAMCaseGenerator.py``` script. All you need to do is to run this script the usual way to generate your case setup:

```bash
python3 OpenFOAMCaseGenerator.py
```

Some additional command line arguments can be used. To see a list of these and their inputs, run the case generator with the ```--help``` flag, e.g.:

```bash
python3 OpenFOAMCaseGenerator.py --help
```

### Running examples

> :warning: This section is outdated, the json file reading has been removed in favour of direct python module parsing. This section will be updated with the full release of version 2.0.0, run the case generator with the --help flag to see the current supported syntax!

To get started, a couple of examples come by default with the case generator. These are located in the ```examples/settings``` directory. To run any of them, we can use the ```--input=path/to/example/case``` command line argument.

To run a compressible flow simulation around the NACA 0012 airfoil at a Reynolds number of Re=6 000 000 and Mach number of Ma=0.15, we can use the following command:

```python
python3 OpenFOAMCaseGenerator.py --input=examples/settings/compressible/airfoil.json
```

To run the same case using an incompressible set up (same Reynolds number), use

```python
python3 OpenFOAMCaseGenerator.py --input=examples/settings/incompressible/airfoil.json
```

To run an unsteady simulations using large Eddy simulations (LES), there is a case prepared for the Taylor-Green Vortex problem which uses custom initial conditions and the c++ source code along with its boiler plate code setup is written to the appropriate files.

To run the case using a compressible solver, use

```python
python3 OpenFOAMCaseGenerator.py --input=examples/settings/compressible/taylorGreenVortex.json
```

For the incompressible version, use

```python
python3 OpenFOAMCaseGenerator.py --input=examples/settings/compressible/taylorGreenVortex.json
```

For both cases, the mesh resolution can be fine tuned in the blockMeshDict file that will be copied into the case directory. By default it is running on 4 processors and all the parallelisation setup and execution is done automatically. At the end, some custom python post-processing functions are executed which will plot the kinetic energy evolution as well as its dissipation over time and compared against reference data. Note that the OpenFOAM solvers are rather dissipative and an explicit Runge Kutta based solver may be a better choice here for better accuracy.

### Storing cases for later reuse

Sometimes we may want to be able to reproduce a case setup at a later stage while setting up some other cases (requiring some input changes which may lose the case setup entirely). To prevent this, there are two additional command line arguments for storing the current case setup to a json file which can later be used to reproduce the case setup by specifying this json file as the ```--input=path/to/json/file``` command line argument.

The option that we have available are ```--output=path/to/json/file/storage/place``` and ```--write-json-only=path/to/json/file/storage/place```. The difference between the two is that the first will write out a json file at the specified location (needs to append the *.json ending at the end) as well as proceed to write out the case setup for OpenFOAM, while the second argument will only proceed to write out the json file but no case setup for OpenFOAM.

### Modifying the input for the case generator

Now that we know how to read and write input files, let us have a look at how we can change the input for the case generator. All input is done within the ```input/CaseProperties.py``` module. Within this module, there is a class called CaseProperties and within the constructor, a dictionary of key value pairs is constructed which is used to generate the case setup. This is the only place where changes to the input should be done.

Most input will require to make a choice from a list of valid parameters. If that is the case (and to avoid typos), the user needs to specify a unique numeric key, rather than a string presenting the choice. The numeric key is specified in the ```input/GlobalVariables.py``` module and accessed through the ```Parameters``` namespace. Where such a choice is required, all options are listed above the choice with a description for each option. To make a choice, we append it to the ```Parameters``` namespace, separated by a dot. For example, within the ```flow_properties```, we can choose the flow to be either incompressible or compressible, the description for that looks as follows:

```python
# type of the flow to solve
#   The following types are supported:
#     incompressible:   Solve the flow using a constant density approach
#     compressible:     Solve the flow using a variable density approach
'flow_type': Parameters.incompressible,
```

### Structure of the properties dictionary

The only place requiring changes during the case setup is the ```CaseProperties``` class' constructor. As alluded to before, we set up a dictionary here of key value pairs that drive the simulation setup. This dictionary contains a range of sub-dictionaries (which in turn may have additional dictionaries) to organise the input into logical pieces. Each of these sub-dictionary within the main case properties dictionary is described below:

- **file_properties:** Specify the case name and where the generated case should be written to. It also deals with how the mesh file is handled and either copies a ```polyMesh``` directory into the ```constant``` directory of the case setup or a corresponding ```blockMeshDict``` and/or a ```snappyHexMeshDict``` into the ```system``` directory.
  
- **parallel_properties:** Specify if the case should be run in parallel and if so, how many processor should be used. This influences the set up of the ```decomposeParDict```, which is used to handle the domain decomposition task. Furthermore, the ```Allrun``` script will receive the correct ```MPI``` command to run the application in parallel with the right number of processors, along with the right command to reconstruct the case back into one once the simulation is finished.
  
- **boundary_properties:** Here we specify the boundary conditions of the case along with some boundary specific setup. We can, for example, specify if we want to use a custom boundary inlet profile (in which case we need to specify the path to the c++ code which to use as the custom boundary condition). Furthermore, we can setup all settings related to the DFSEM inlet boundary condition (useful for LES simulations with open boundaries), however, the use is discouraged as the implementation seems buggy and not fixed yet. **IMPORTANT:** When generating the mesh (blockMesh, snappyHexMesh, external tool), make sure that wall patches have the type WALL, empty patches the type EMPTY and **EVERYTHING ELSE** is set to patch (i.e. even symmetry patches should be set to patch). If this is not done you may encounter errors when running OpenFOAM. 

- **flow_properties:** This is where we set the flow properties of the fluid such as the velocity, pressure, viscosity, temperature and density at open (inlet) boundaries. We can either specify these dimensional units, or, use non-dimensional quantities such as the Reynolds and Mach number to steer the simulation setup. Depending on which setting is set (i.e. dimensional or non-dimensional quantities), the other set that is not specified will be computed from the provided input. In addition, this place also handles the initial conditions and we are able to use custom initial conditions where we need to, again, specify the location of the c++ script that shoulod be used for the custom initial conditions.

- **solver_properties:** This entry handles all input around the solver that needs to be used, along with information on when to start and for how long to run it. Under-relaxation is also specified here which essential determines the convergence rate of the solver (or divergence if set too high). 

- **numerical_discretisation:** Here we can only make a few choices, whether the case is steady or unsteady, whether to use first-order for turbulent quantities when solving RANS models and, most important of all, which discretisation policy to use. Here we essential steer the behaviour of our flow and we can choose between a default, robust, accurate and total-variation diminishing (TVD) approach. This will set sensible default values which can be fine tuned if required by the case.

- **turbulence_properties:** This sub-dictionary specifies the turbulence model that should be used. For RANS simulations, all OpenFOAM supported models can be chosen (i.e. those based on linear and non-linear eddy viscosity models, transitional model, Reynolds stresses-based models as well as scale adaptive-based models). When using RANS, calculating initial conditions for all boundary files can be a daunting task. Each variable needs to be specified for each boundary condition which adds a minimum of two files (variables) to the zero directory for which initial and boundary conditions can be specified. Commercial solvers like ANSYS Fluent take responsibility away here from the user by asking them to provide engineering properties that can be easily accessed or at least reasoned about (e.g. the freestream turbulence intensity). The same approach is taken here and a further simplification over ANSYS Fluent, for example, is taken, in that the wall modelling approach does not need to be explicitly defined but rather the intention should be stated, i.e. if the wall should be resolved (the y+ value should be one or less, here indicated as a low Reynolds number modelling approach) or if wall functions should be used (the y+ value should be within the log layer, i.e. greater than 30, here indicated as a high Reynolds number modelling approach). Along with this, the type of flow needs to be prescribed (internal or external) from which the turbulent length scale is calculated, together with the freestream turbulence intensity and characteristic length. If the flow can not be classified as such, the turbulent to laminar ratio can be prescribed instead or left to be calculated on the freestream turbulence intensity entirely if such a statement can not be made. In addition to RANS, full support for LES and DES (DDES, IDDES) simulations are supported and the user can choose these here as well with all required options.

- **convergence_control:** Here we control the overall convergence behaviour of the simulation. In total there are three parts to this. First, we can specify an overall convergence parameter which is used to check if the simulation has converged to a prescribed threshold (typically used for steady state simulations). Then we also need to specify the convergence threshold for all inner iterations (which will be used to judge convergence for each iteration for all implicit matrix solvers). These will not influence if the simulation should be stopped but rather steer only the inner (not outer) iterations. Finally, we can prescribe a convergence parameter based on integral quantities (such as the lift or drag coefficient) and we can choose an arbitrary number of force coefficients to monitor simultaneously (for example, it is common to use both lift and drag to judge convergence). If these do not change within a user-specified averaging window below a certain convergence threshold, the simulation is deemed converged (and stopped), even if the solver itself has not converged to a user specified convergence criterion. 
  
- **dimensionless_coefficients:** Here we can specify if we want to calculate non-dimensional force coefficients, as well as pressure coefficients and wall shear stresses (which can, in turn, be used to calculate the skin friction coefficient). All required input is done here, expect for the lift, drag and pitch axis, which is calculated from the **flow_properties** inputs, where we have to specify the **axis_aligned_flow_direction**. Based on this input, the lift, drag and pitch axis can be uniquely identified. The setup of the **dimensionless_coefficients** is required if these should be used to judge convergence, as specified in the **convergence_control** dictionary. 
  
- **additional_fields:** This entry allows us to write out additional quantities during the calculation. For compressible flows, the Mach number is automatically set up so no additional change is required here. Currently,Vorticity, Enstrophy, the Q and Lambda2-criterion are supported. The additional field(s) that should be written out are specified as a list and more than one additional field can be written out. You can specify an additional field here and use it later (in the iso surfaces, for example) to create a plot using the variable specified here, i.e. the order of setup is important for OpenFOAM (the additional fields need to be specified before) which is automatically taken care of here.

- **point_probes:** This presents the possibility to prescribe points in the flow field to monitor specific quantities. This may be useful if certain locations in a domain have experimental data available for which comparions can be made. Additionally, for scale resolved turbuent simulations we can use these point probes as inputs for energy sepctra calculations.  

- **line_probes:** Just like the point probes, this utility allows us to monitor a quantity along a prescribed line, useful for generating profiles for monitored quantities.
  
- **cutting_planes:** Cutting planes are useful for larger simulations where we know in advanced which planes we want to examine. For RANS simulations, this may not necessarily be an advantage (as we only get one timestep, i.e. the steady state solution), for any unsteady simulations, however, especially scale resolved 3D simulations, we can use this cutting plane feature to extract only 2D planes at locations of interest which we can then use for either further time-dependent post processing or to generate an animation of the flow. The files will be written out to the post-processing directory and are, by default, rather inaccessible (each plane needs to be loaded separately). To automate that process, each time a cutting plane is requested, a python utility script is also copied into the case setup which will generate a master VTP file which contains all the locations of the individual planes. We only need to load this VTP file in paraview which will give us access to all the individual cutting planes. This utility script is also added to the ```Allrun``` script so that the user does not need to do anything extra, this is all handled automatically.
  
- **iso_surfaces:** ISO surfaces are useful for 3D simulations to monitor the flow of a specific quantity. A classical example is that of ISO surfaces of the Q-criterion. Traditionally, we would need to store all 3D solutions for the duration for which the iso surfaces should be monitored (and perhaps be used for generating an animation). This can quickly escalate and results in a rather large storage requirement. To circumvent this, we can specify here ISO contours we would like to write out during the simulation along with additional fields on these ISO surfaces so that we can colour them accordingly during post processing. This reduces the computational storage requirement significantly and we can store longer periods of time during which we would like to observe a quantity. The setup is done in such a way that we can specify a number of variables for which we would like to write out ISO surfaces. However, we can also specify the same variable several times if we want to observe only one variable but with different ISO values (for example, if the exact ISO value can not be fully reasoned about beforehand). Similar to the cutting planes described above, the ISO surfaces are written out in an inaccessible format (requiring all surfaces to be loaded individually). Thus, the same utility script, which is also used for the cutting planes, is copied into the case setup and used to generate a global VTP file which can then easily load all required surfaces into paraview.

- **post_processing:** OpenFOAM offers a range of post-processing function objects. On top of that, there may be certain user-defined post-processing scripts that we may want to run once the simulation is done. The post_processing dictionary allows for exactly that. We can write all function objects in one file and then point to it within the function_objects dictionary. Similarily, we can also copy custom made python scripts to the case setup along with additional files that are required by the python script. For example, we may wish to compare experimental results with our OpenFOAM solution, in this case we may wish to copy experimental data, stored within text files, into our case setup along with the python script. All python scripts will be added to the Allrun file so that post-processing is done automatically after the simulation is done.

### Protection against common mistakes

It is easy to set up a simulation which provides a perfectly acceptable case setup and which will run in OpenFOAM which is, however, non-physical or is deemed to give inaccurate results. For this, a case checking utility is implemented which will prevent the user from setting up the case with wrong settings. For example, there is no point to say we want to perform an LES simulation with a steady state solver, or, specify the flow to be compressible but then requesting an incompressible solver. These checks are implemented to help the user avoid common pitfalls and, depending on the severity of the situation, either a warning or error (which will then abort the case setup) will be issued. This is similar to the ANSYS Fluent check case but more pertinent to OpenFOAM specific settings.

### Known limitations

> :warning: Any path you specify in the *properties* dictionary should be defined using the ```os.path.join('path', 'to', 'join')``` command, which in turn will write out json files where paths are represented either with ```\ ``` (windows) or ```/``` (unix). The examples have been prepared using windows, thus you may want to change the json files to have unix-styled paths if you encounter problems here.

## License

This software is provided under the MIT license, see the accompanying license file.

## Contributions / Issues

Unit testing such a case generator is a difficult endeavour as most unit tests would need to test files that are written out to disk which, in turn, result in brittle tests (all it takes is for OpenFOAM to change the name of a parameter to make unit tests fail). Therefore, unit tests are avoided but replaced by system tests (which are provided in the ```examples``` directory). It is these examples that should be checked for physically correct results to ensure a correct case setup is performed, which provides a much stronger confidence.

There will be, however, cases, where not all possible OpenFOAM specific settings are tested down to their last detail. While all settings were tested during implementation to ensure the case setup would run, there will be boundary cases which have not been tested. Additionally, it is possible that undetected bugs still linger in the source code. If you find such deficiencies, please open an issue here on github. Alternatively, if this is something quick to fix, consider making a contribution and perform a pull request. Contributions by the community are actively encouraged.