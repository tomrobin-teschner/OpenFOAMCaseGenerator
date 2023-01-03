# Cylinder

This case sets up the flow around a cylinder for a Reynolds number of 100 using an incompressible assumption and an unsteady discretisation. A background mesh is generatede with blockMeshDict and the cylidner is injected using snappyHexMesh.

# Usage

To set up the case, use the following command:

```bash
python3 OpenFOAMCaseGenerator.py --input=Cylinder
```