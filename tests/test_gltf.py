import os
import sys
import unittest
import pathlib
import glglue.gltf


GLTF_SAMPLE_DMODELS = pathlib.Path(os.environ['GLTF_SAMPLE_MODELS'])
if not GLTF_SAMPLE_DMODELS.exists():
    sys.exit()


class TestGltf(unittest.TestCase):

    def test_glb(self):
        path = GLTF_SAMPLE_DMODELS / '2.0/Box/glTF-Binary/Box.glb'
        self.assertTrue(path.exists())
        json, bin = glglue.gltf.parse_glb(path.read_bytes())
        self.assertTrue(json)
        self.assertTrue(bin)
        gltf_data = glglue.gltf.parse_gltf(json, bin)  # type: ignore
        self.assertEqual(1, len(gltf_data.materials))
        self.assertEqual(1, len(gltf_data.meshes))
        self.assertEqual(
            24, gltf_data.meshes[0].primitives[0].position.count())
        # type: ignore
        self.assertEqual(24, gltf_data.meshes[0].primitives[0].normal.count())
        # type: ignore
        self.assertEqual(36, gltf_data.meshes[0].primitives[0].indices.count())
        self.assertEqual(2, len(gltf_data.nodes))


if __name__ == '__main__':
    unittest.main()
