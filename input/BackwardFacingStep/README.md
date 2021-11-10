# Backward Facing Step

This case provides the case setup for the incompressible flow over a backward facing step at a Reynolds number of Re=36,000 (based on the step height H) and is based on the experiments of *Driver, D. M. and Seegmiller, H. L., "Features of Reattaching Turbulent Shear Layer in Divergent Channel Flow," AIAA Journal, Vol. 23, No. 2, Feb 1985, pp. 163-171.*.

This case is part of NASA's Turbulence Modeling Resources and a full description can be founbd here: [https://turbmodels.larc.nasa.gov/backstep_val.html](https://turbmodels.larc.nasa.gov/backstep_val.html)

The case setup is provided with the kOmega-SST RANS model and two grids are provided (coarse and fine), which the user can choose from. These grids were converted from the [provided grids by NASA](https://turbmodels.larc.nasa.gov/backstep_grids.html) and correspond to the following resolutions:

- Fine: 2x257x257, 2x97x257, 2x385x449, 2x129,449
- Coarse: 2x33x33, 2x13x33, 2x49x57, 2x17x57

# Usage

To set up the case, use the following command, which will by default use the fine grid:

```bash
python3 OpenFOAMCaseGenerator.py --input=BackwardFacingStep
```

To use the coarse grid, you can either change the ```BackwardFacingStep.py``` module or overwrite the meshing parameter as follows:

Unix:
```bash
python3 OpenFOAMCaseGenerator.py --input=BackwardFacingStep --replace=file_properties/polymesh_directory:examples/mesh/backwardFacingStep/coarse
```

Windows:
```bash
python3 OpenFOAMCaseGenerator.py --input=BackwardFacingStep --replace=file_properties/polymesh_directory:examples\\mesh\\backwardFacingStep\\coarse
```

# Expected results

As part of this case setup, experimental data has been digitised and will be plotted against the numerical results at the end of the simulation. There will be 3 plots that will be generated, named:

- **postProcessing/skin_friction_profile.png**: Plots the skin friction coefficient along the main channel's bottom wall and compares that against experimental measurements.

- **postProcessing/inlet_velocity_profile.png**: Plots the velocity profile at x/H=-4 and compares that to experimental measurements. It is crucial to get this profile right as the reference velocity is specified at the channel's centerline at x/H=-4 rather than at the boundary.

- **postProcessing/velocity_profiles.png**: This will plot the velocity profiles in the main channel and compare that against experimental measurements at x/H=1, 4, 6 and 10.

In addition, the reattachment location will be printed to screen, which is x/H=6.28 +-0.10 according to the experiment. 