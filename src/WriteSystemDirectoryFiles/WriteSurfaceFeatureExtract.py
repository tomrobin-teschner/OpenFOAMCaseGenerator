import os


class WriteSurfaceFeatureExtract:
    def __init__(self, properties, file_manager):
        self.properties = properties
        self.file_manager = file_manager

    def write_surface_feature_extract(self):
        file_id = self.file_manager.create_file('system', 'surfaceFeatureExtractDict')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'yPlus')
        self.file_manager.write(file_id, '\n')
        for geometry in self.properties['file_properties']['snappyhexmeshdict']['geometry']:
            self.file_manager.write(file_id, os.path.basename(geometry) + '\n')
            self.file_manager.write(file_id, '{\n')
            self.file_manager.write(file_id, '    // How to obtain raw features (extractFromFile || extractFromSurface)\n')
            self.file_manager.write(file_id, '    extractionMethod    extractFromSurface;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    // Mark edges whose adjacent surface normals are at an angle less\n')
            self.file_manager.write(file_id, '    // than includedAngle as features\n')
            self.file_manager.write(file_id, '    // - 0  : selects no edges\n')
            self.file_manager.write(file_id, '    // - 180: selects all edges\n')
            self.file_manager.write(file_id, '    includedAngle       150;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    subsetFeatures\n')
            self.file_manager.write(file_id, '    {\n')
            self.file_manager.write(file_id, '        // Keep nonManifold edges (edges with >2 connected faces)\n')
            self.file_manager.write(file_id, '        nonManifoldEdges    no;\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '        // Keep open edges (edges with 1 connected face)\n')
            self.file_manager.write(file_id, '        openEdges           yes;\n')
            self.file_manager.write(file_id, '    }\n')
            self.file_manager.write(file_id, '\n')
            self.file_manager.write(file_id, '    // Write features to obj format for postprocessing\n')
            self.file_manager.write(file_id, '    writeObj            no;\n')
            self.file_manager.write(file_id, '}\n')
            self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')
