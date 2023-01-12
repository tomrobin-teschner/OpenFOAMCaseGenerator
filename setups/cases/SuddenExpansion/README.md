# Flow through a suddenly increasing channel

This case provides the setup for a suddenly expanding channel. Here, a smaaller channel expands instantaneously into a larger one (symmetrically) but for a given critical Reynolds number, the flow will provide a non-symmetric flow field, non as the bifurcation phenomenon. This work is based on the following reference paper:

R. M. Fearn, T. Mullin, and K. a. Cliffe, "Nonlinear flow phenomena in a symmetric sudden expansion," Journal of Fluid Mechanics, vol. 211, no. -1, p. 595, 1990.

The critical Reynolds number at which the bifurcation is expected is Re=54, based on the step height of the suddenly expanding channel. In order to ensure that the flow is sufficiently developed as it enters the enlarged channel, the development length of the flow is calculated based on the Reynolds number and used to size the channel during mesh generation. Further details are provided in the blockMeshDict file.

# Usage

To set up the case, use the following command:

```bash
python3 OpenFOAMCaseGenerator.py --input=SuddenExpansion
```

# Expected results

Velocity profiles are provided for

* x/h = 1.25
* x/h = 2.5
* x/h = 5.0
* x/h = 10.0

where h is the step height of the suddenly expanding channel. They show a non-symmetric flow field in the velocity components of U. The reattachment point at the upper and lower channel wall should be at

* x/h = 3.658
* x/h = 10.060

based on the work of:

P. J. Oliveira, "Asymmetric flows of viscoelastic fluids in symmetric planar expansion geometries," Journal of Non-Newtonian Fluid Mechanics, vol. 114, no. 1, pp. 33(63), 2003.

Note that either attachment point can occur at both upper and lower wall, although it is expected that the flow will reattach at the bottom wall sooner as the flow is initialised with a non-symmetric flow field to force bifurcation. This approach provides faster computational results but must be deactivated when trying to find the critical Reynolds number to let the bifurcation occur naturally.