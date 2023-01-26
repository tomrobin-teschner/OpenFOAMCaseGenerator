# Taylor-Green Vortex problem

This case setup is for the Taylor-Green Vortex problem, a 3D cubed domain of length 2*pi in each direction with reference length L=1.

# Usage

To set up the case, use the following command:

```bash
python3 OpenFOAMCaseGenerator.py --input=TaylorGreenVortex
```

Use the provided ```Allrun``` and ```Allclean``` script ro run the simulation and post-processing routines as well as to clean up the case once the calculation is done.

# Expected results

This case comes with custom functionObjects and python post-processing routines. The function objects will calculated the volume integrated kinetic energy of the instantaneous velocity field which is then used by the python post-processing routines to plot the decay of the kinetic energy, as well as calculate its dissipation rate which is also plotted. These plots are available in the postProcessing folder within the case's root directory after the calculation is done.