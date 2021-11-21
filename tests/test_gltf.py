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
            24, gltf_data.meshes[0].primitives[0].position.get_count())
        self.assertEqual(
            24, gltf_data.meshes[0].primitives[0].normal.get_count())
        self.assertEqual(
            36, gltf_data.meshes[0].primitives[0].indices.get_count())
        self.assertEqual(
            'Red', gltf_data.meshes[0].primitives[0].material.name)
        self.assertEqual(2, len(gltf_data.nodes))

    def test_glb(self):
        path = GLTF_SAMPLE_DMODELS / '2.0/BoxTextured/glTF-Binary/BoxTextured.glb'
        gltf_data = glglue.gltf.parse_path(path)
        self.assertEqual(1, len(gltf_data.materials))
        self.assertEqual(1, len(gltf_data.meshes))
        self.assertEqual(
            24, gltf_data.meshes[0].primitives[0].position.get_count())
        self.assertEqual(
            24, gltf_data.meshes[0].primitives[0].normal.get_count())
        self.assertEqual(24, gltf_data.meshes[0].primitives[0].uv0.get_count())
        self.assertEqual(
            36, gltf_data.meshes[0].primitives[0].indices.get_count())
        self.assertEqual(
            'Texture', gltf_data.meshes[0].primitives[0].material.name)
        self.assertEqual('CesiumLogoFlat.png',
                         gltf_data.textures[0].image.name)
        self.assertEqual(glglue.gltf.MimeType.Png,
                         gltf_data.textures[0].image.mime)
        self.assertEqual(2, len(gltf_data.nodes))

    def test_all(self):
        dir = GLTF_SAMPLE_DMODELS / '2.0'
        for model in dir.iterdir():
            if not model.is_dir():
                continue
            for kind in model.iterdir():
                if not kind.is_dir():
                    continue
                for path in kind.iterdir():
                    match path.suffix:
                        case '.gltf':
                            gltf_data = glglue.gltf.parse_path(path)
                        case '.glb':
                            gltf_data = glglue.gltf.parse_path(path)


if __name__ == '__main__':
    unittest.main()
