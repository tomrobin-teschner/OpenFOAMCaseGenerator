# Lid Driven Cavity

This case sets up the flow inside a lid driven cavity for incompressible solvers. It comes with a post-processing utility script that plots results obtained from OpenFOAM as well as reference data taken from *U Ghia, K.N Ghia, C.T Shin, "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method", Journal of Computational Physics, Vol. 48, No. 3, 1982, pp. 387-411* for specific Reynolds numbers of Re=100, 400, 1000, 3200, 5000, 7500, 10000. The ```Allrun``` script will ensure that the correct plots are generated, as long as the correct Reynolds number is specified in the case setup file (there are two places where the Reynolds number needs to be set, once in the case setup for the flow properties and once for the post-processing where it is passed as an argument to the script)

# Usage

To set up the case, use the following command, which will by default use the fine grid:

```bash
python3 OpenFOAMCaseGenerator.py --input=LidDrivenCavity
```

You can then run the case using the provided ```Allrun``` script. 

# Expected results

If the provided ```Allrun``` script is used and a Reynolds number is provided for which there is reference data available, a corresponding plot of the velocity profiles will be generated which will be available within the ```postProcessing``` folder.