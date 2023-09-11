[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Generic badge](https://img.shields.io/badge/Version-v3.0.0beta.1-red.svg)](https://shields.io/)

## Overview

Creating an OpenFOAM simulation typically involves copying and pasting of existing tutorial files and modifying them for ones need. There are several issues with this approach. For starters, it is an error prone approach and one of the first thing programmers learn, do not copy and paste. It is just bad practice. You may change the required parameter to suit your case setup, but OpenFOAM is so complex that we can set a myriad of parameters. Parameters we don't know or recognise, may remain unchanged and introduce critical mistakes in our case setup which will result in incorrect results.

The OpenFOAMCaseGenerator aims to avoid this by creating a sensible case setup from scratch, without the need to copy and paste simulation parameters. It is driven by a single python-based input file, that allows some further processing of the input parameter, which allows for complete parameterisation of the case setup. Changing one parameter now is a simple as changing a command line argument to the case generator script, which in turn will take care of writing out the correct case setup.

Furthermore, the OpenFOAMCaseGenerator is not simply mirroring the case setup inside a single python file, but rather aims to capture intent, instead of detailed input. For example, the numerical schemes are set up based on accuracy requirements and based on which discretisation policy is set, the best possible default values are chosen.

Testing is a core concept in software development, and the OpenFOAMCaseGenerator comes baked in with unit and system tests to ensure the correct working of the provided case setup.

## Documentation

The latest documentationc an be found at [Read the docs](https://openfoamcasegenerator.readthedocs.io/en/latest/).

## Quickstart

To see all available cases shipped with the case generator, run it with the ```--list-cases``` command line argument.

```bash
python3 OpenFOAMCaseGenerator.py --list-cases
```

To see all available command line arguments and a short description for each, run it with the ```--help``` argument, i.e.

```bash
python3 OpenFOAMCaseGenerator.py --help
```

To setup a case, you need to pass one additional command line argument: ```--case=case_name```. This tells the case generator which case setup to generate. The input file is specific for each case and example case setups can be found in the ```input/cases``` directory. So, to generate the case for the Naca0012 airfoil, run the following command

```bash
python3 OpenFOAMCaseGenerator.py --case=Naca0012
```

This will show all available case setups in the ```input/cases``` folder and may be more convenient to use.

Each case comes with a few parameters that are case specific and that we can fine-tune. For example, if we run the Naca0012 aerofoil example, we will see the following output

```bash
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
```

We can see at the bottom that we can fine-tune parameters that make sense for this case, such as the angle of attack and the reynolds number. If we wanted to change any of these, we simply tun the case generator again and pass either the ```--parameter:key=value``` or ```-p:key=value``` construct, where the key is the name listed in the parameter list (for example, ```reynolds_number```) and the ```value``` is the value we want to set this parameter to. If we wanted to change the angle of attack to 10 degrees, for example, we would invoke the case generator as

```bash
python3 OpenFOAMCaseGenerator.py --case=Naca0012 --parameter:angle_of_attack=10
```

or

```bash
python3 OpenFOAMCaseGenerator.py --case=Naca0012 -p:angle_of_attack=10
```

To learn more about how to set up your own custom case setup, consult the documentation on [setting up cases](https://openfoamcasegenerator.readthedocs.io/en/latest/usage.html#).

## License

This software is provided under the MIT license, see the accompanying license file.
