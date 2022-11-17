import unittest
import glglue.util


class TestUtils(unittest.TestCase):

    def test_utils(self):
        self.assertEqual(1.5, glglue.util.get_desktop_scaling_factor())


if __name__ == '__main__':
    unittest.main()
