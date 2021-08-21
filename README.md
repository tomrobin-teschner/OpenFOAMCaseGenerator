[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Generic badge](https://img.shields.io/badge/Version-v1.2.7-red.svg)](https://shields.io/)

## Introduction

This collection of python files will generate a basic case set-up for openfoam, i.e. it will generate the **0/**, **constant/** and **system/** directory with all required files based on some user input.
Note that this is for the ESI version of OpenFOAM (www.openfoam.com) and not the foundation (www.openfoam.org) version.
Most of the case set-up may still work but some smaller details may differ in the two different version. You have been warned.
Some features that are used in this case generate script may require an up-to-date version of OpenFOAM. The version used here for testing is v2006.

The idea is that a lot of files can be automatically written based on some basic information provided by the user.
For example, by specifying the turbulence model that should be used, along with the intention of using a High-Reynolds number (y+>30) or Low-Reynolds number (y+~1) modelling approach, the boundary files can be uniquely determined and written automatically with some more informative user-input, for example the reference length and free-stream turbulent intensity (rather than having to calculate all turbulent properties manually).
The user only has to specify the name and type of boundary and the rest is handled by the script. In-fact, all possible files are written so that on can easily switch from one turbulence model to another, without having to modify the **0/** directory.

Numerical schemes are handled in a similar manner, instead of having to specify numerical discretisation schemes for each flow variable, sensible default discretisation approaches are presented and the user only has to specify which numerical discretisation *policy* should be used.
In the case of the different policies that are available, for example, the user can choose between *DEFAULT*, *TVD*, *ROBUST* and *ACCURACY*.
The *DEFAULT* policy is recommended, for example, for most types of simulations but on could change that to *ROBUST* if convergence problems are encountered.
Equally, it can be changed to *ACCURACY* if a higher-order accuracy is sought (for scale-resolved simulations, for example).

## Usage

To get started, you can run the example case provided with this distribution. This will set up the flow for the flow around a NACA 0012 airfoil at a Reynolds number of 6 million at an angle of attack of 0 degrees. This should result in a lift coefficient value c_l = 0 and a drag coefficient value of c_d = 0.008.

To run the example, simply specify which input script you want to use

```bash
python3 OpenFOAMCaseGenerator.py --input=examples\settings\airfoil.json
```

This will generate a case directory setup called ```NACA_0012_kw_SST_y+_1_Re_6e6``` within the root folder of this case generator. You can open this folder and run OpenFOAM within it.

To prepare your own cases, you will need to modify the *properties* dictionary in the *OpenFOAMCaseGenerator.py* file, which is defined at the top of the script within the ```case_properties()``` function.

The *properties* dictionary has sub-dictionaries defined as follows:

- **file_properties:** Specify the case name and where the generated case should be written to
- **parallel_properties:** Specify if the case should be run in parallel. Additional files will be written in this case.
- **boundary_properties:** Here the user has to specify the name of the boundary patches along with their properties. **IMPORTANT:** When generating the mesh (blockMesh, snappyHexMesh, external tool), make sure that wall patches have the type WALL, empty patches the type EMPTY and **EVERYTHING ELSE** is set to patch (i.e. symmetry patches should also be set to patch. May change in the future, in this case this README file will be updated)
- **flow_properties:** Set inlet velocity, viscosity, etc.
- **solver_properties:** Select the solver to be used (only incompressible supported at the moment, compressible solver planed and will follow shortly. Once they are available this README file will change accordingly). This dictionary is essentially used to generate the controlDict file, but you can also specify under-relaxation factors here.
- **numerical_discretisation:** This dictionary is used to set the discretisation policy as alluded to in the introductory section above.
- **turbulence_properties:** Set the required turbulence model (RANS or LES). It will generate the appropriate turbulenceTransport file within the constant/ directory with all required entries.  
- **convergence_control:** Here you can specify the convergence parameter for your implicit solvers (inner iterations), but also the overall convergence threshold (outer iterations). Additionally, you have to option to specify a integral quantity (lift or drag coefficient, for example) to monitor and judge convergence based on its behaviour. Useful where these properties can be defined.
- **dimensionless_coefficients:** Dictionary that specifies the reference values for the calculation of the force coefficients (and pressure coefficient). You can also specify here if force and pressure coefficient, as well as wall shear stresses should be calculated during the simulation. Force coefficient computations is required if you want to judge convergence based on non-dimensional force coefficients.
- **additional_fields:** This will allow you to compute additional flow fields. Currently supported: Vorticity, Enstrophy, Q-criterion, Lambda2-criterion. More than one filed can be written at the same time.
- **point_probes:** Allows to output flow information at single points in the flow field (useful for scale resolved simulations)
- **line_probes:** Like point_probes, output additional information at run-time, only here write out information along a 1D line. Useful to get velocity profiles.
- **cutting_planes:** Like point_probes and line_probes, output 2D cutting planes of the flow-field.
- **iso_surfaces:** Output iso-surfaces of the flow-field. Can use the additional fields that are calculated, for example, the Q-criterion for turbulent flow-structure visualisation.

One thing to note here is that most of these dictionaries have a range of accepted input variables that can be specified.
For example, the **boundary_properties** dictionary can only work with a number of boundary conditions. If this is the case, then the user has the choice to specify these through the *Parameters* variable.
These are global variables that will uniquely identify a certain input to avoid misspelling words in the input file. For example, consider this simple example with 4 boundary conditions, the **boundary_properties** dictionary could look as follows:

```python
'boundary_properties': {
    'inlet': Parameters.INLET,
    'outlet': Parameters.BACKFLOW_OUTLET,
    'wall': Parameters.WALL,
    'frontAndBack': Parameters.EMPTY,
},
```
Whenever there is a range of choices that can be specified through the *Parameters* variable, all available options are listed as options. The idea is that these can be simply copy and pasted as required so as to avoid having spelling mistakes, which can make debugging the case file sometimes unnecessarily unpleasant.

Within the **file_properties** sub-dictionary, you can specify where the mesh directory is located. If you specify it here then the case generator script will copy the mesh over to the generated case setup. If you leave this field empty, no mesh will be copied and you have to manually copy and paste the *polyMesh* directory into the *constant/* directory.

There are additional command line arguments that can be specified to steer the behaviour of the case generator, these are listed below:

```
--help                      prints this help menu
--input=name                select a input file to use instead of the properties set in the code
--output=name               output a json script along with the case setup as specified by the properties dictionary
--write-json-only=name      output the case to a json file only, don't write the case setup
```

We have already seen the ```--input``` flag above which let's us run an already prepared case setup. If we want to preserve the our current setup, we can specify either the ```--output``` flag (which will save the properties into a json file and generate the case setup for us) or the ```--write-json-only``` flag which will only output the case setup to a json file without generating the actual case setup.

> :warning: **Note:** any path you specify in the *properties* dictionary should be defined using the ```os.path.join('path', 'to', 'join')``` command, which in turn will write out json files where paths are represented either with ```\ ``` (windows) or ```/``` (unix). The examples have been prepared using windows, thus you may want to change the json files to have unix-styled paths if you encounter problems here.

## License

This piece of software is provided under the MIT license, see the accompanying license file.

## Contributions / Issues

There will be, unavoidably, bugs that will come up with certain parameter combinations.
While validation cases were run to ensure the correctness of most settings, it is impossible to test all possible combinations.
Should you feel that some things are incorrectly set-up, please open an issue here on github for others to benefit from.
You may also want to open a pull-request if you feel you have done some modifications that can be useful for others to have.
