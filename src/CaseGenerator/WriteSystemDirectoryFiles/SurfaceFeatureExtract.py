import os
from src.CaseGenerator.FileDirectoryIO import WriteHeader


class SurfaceFeatureExtract:
    def __init__(self, properties):
        self.properties = properties

    def get_file_content(self):
        version = self.properties['file_properties']['version']
        surf_extract = WriteHeader.get_header(version, 'dictionary', 'system', 'surfaceFeatureExtractDict')
        for geometry in self.properties['file_properties']['snappyhexmeshdict']['geometry']:
            surf_extract += f'{os.path.basename(geometry)}\n'
            surf_extract += f'{{\n'
            surf_extract += f'    // How to obtain raw features (extractFromFile || extractFromSurface)\n'
            surf_extract += f'    extractionMethod    extractFromSurface;\n'
            surf_extract += f'\n'
            surf_extract += f'    // Mark edges whose adjacent surface normals are at an angle less\n'
            surf_extract += f'    // than includedAngle as features\n'
            surf_extract += f'    // - 0  : selects no edges\n'
            surf_extract += f'    // - 180: selects all edges\n'
            surf_extract += f'    includedAngle       150;\n'
            surf_extract += f'\n'
            surf_extract += f'    subsetFeatures\n'
            surf_extract += f'    {{\n'
            surf_extract += f'        // Keep nonManifold edges (edges with >2 connected faces)\n'
            surf_extract += f'        nonManifoldEdges    no;\n'
            surf_extract += f'\n'
            surf_extract += f'        // Keep open edges (edges with 1 connected face)\n'
            surf_extract += f'        openEdges           yes;\n'
            surf_extract += f'    }}\n'
            surf_extract += f'\n'
            surf_extract += f'    // Write features to obj format for postprocessing\n'
            surf_extract += f'    writeObj            no;\n'
            surf_extract += f'}}\n'
            surf_extract += f'\n'
            surf_extract += f'// ************************************************************************* //\n'
        return surf_extract
