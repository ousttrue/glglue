import unittest
import glglue.utils


class TestUtils(unittest.TestCase):

    def test_utils(self):
        self.assertEqual(1.5, glglue.utils.get_desktop_scaling_factor())


if __name__ == '__main__':
    unittest.main()
