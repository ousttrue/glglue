import os
import sys
import unittest
import pathlib
import glglue.gltf


GLTF_SAMPLE_DMODELS = pathlib.Path(os.environ['GLTF_SAMPLE_MODELS'])
if not GLTF_SAMPLE_DMODELS.exists():
    sys.exit()


class TestGltf(unittest.TestCase):

    def test_gltf(self):
        path = GLTF_SAMPLE_DMODELS / '2.0/Box/glTF/Box.gltf'
        gltf_data = glglue.gltf.parse_path(path)
        self.assertEqual(1, len(gltf_data.materials))
        self.assertEqual(1, len(gltf_data.meshes))
        self.assertEqual(
            24, gltf_data.meshes[0].primitives[0].position.count())
        self.assertEqual(24, gltf_data.meshes[0].primitives[0].normal.count())
        self.assertEqual(36, gltf_data.meshes[0].primitives[0].indices.count())
        self.assertEqual(2, len(gltf_data.nodes))

    def test_glb(self):
        path = GLTF_SAMPLE_DMODELS / '2.0/Box/glTF-Binary/Box.glb'
        gltf_data = glglue.gltf.parse_path(path)
        self.assertEqual(1, len(gltf_data.materials))
        self.assertEqual(1, len(gltf_data.meshes))
        self.assertEqual(
            24, gltf_data.meshes[0].primitives[0].position.count())
        self.assertEqual(24, gltf_data.meshes[0].primitives[0].normal.count())
        self.assertEqual(36, gltf_data.meshes[0].primitives[0].indices.count())
        self.assertEqual(2, len(gltf_data.nodes))


if __name__ == '__main__':
    unittest.main()
