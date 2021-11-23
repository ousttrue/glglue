import unittest
import pathlib
import glglue.ktx2


def get_path(key: str) -> pathlib.Path:
    import os
    value = os.environ.get(key)
    if not value:
        import sys
        sys.exit()
    return pathlib.Path(value)


GLTF_SAMPLE_ENVIRONMENTS = get_path('GLTF_SAMPLE_ENVIRONMENTS')


class TestKtx2(unittest.TestCase):

    def test_ktx2(self):
        path = GLTF_SAMPLE_ENVIRONMENTS / 'chromatic/charlie/sheen.ktx2'
        self.assertTrue(path.exists())
        ktx2 = glglue.ktx2.parse_path(path)
        self.assertTrue(ktx2)


if __name__ == '__main__':
    unittest.main()
