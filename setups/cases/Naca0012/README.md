# NACA 0012

This case sets up the flow around a NACA 0012 flow for a compressible fluid at a Mach number of Ma=0.15 and a Reynolds number of Re=6,000,000. The angle of attack is set to 0 but can be changed easily in the case setup file. The reference data are taken from NASA's Turbulence Modelling Resources and the case setup and its detailed description can be found here: [https://turbmodels.larc.nasa.gov/naca0012_val.html](https://turbmodels.larc.nasa.gov/naca0012_val.html)

# Usage

To set up the case, use the following command:

```bash
python3 OpenFOAMCaseGenerator.py --input=Naca0012
```

# Expected results

For an angle of attack of 0, we expect a lift coefficient of 0 (or around zero) and a drag coefficient of around 0.0081.
