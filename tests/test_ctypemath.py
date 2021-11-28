import unittest
from glglue.ctypesmath import Float3


class TestCtypeMath(unittest.TestCase):

    def test_float3(self):
        self.assertEqual(Float3(2, 3, 4), Float3(1, 2, 3) + Float3(1, 1, 1))


if __name__ == '__main__':
    unittest.main()
