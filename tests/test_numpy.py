import unittest
import numpy


class TestNumpy(unittest.TestCase):

    def test_row_vec(self):
        a = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 2, 3, 1],
        ])
        b = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 2, 3, 1],
        ])
        c = a @ b
        v = c[3]
        self.assertTrue((numpy.array([2, 4, 6, 1]) == v).all())

        apply = numpy.array([0, 0, 0, 1]) @ c
        self.assertTrue((numpy.array([2, 4, 6, 1]) == apply).all())

    def test_col_vec(self):
        a = numpy.array([
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ])
        b = numpy.array([
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ])
        c = a @ b
        v = c[:, 3]
        self.assertTrue((numpy.array([2, 4, 6, 1]) == v).all())

        apply = c @ numpy.array([0, 0, 0, 1])
        self.assertTrue((numpy.array([2, 4, 6, 1]) == apply).all())

    def test_type(self):
        a = numpy.array([
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ])
        print(a, type(a))
        self.assertIsInstance(a, numpy.ndarray)


if __name__ == '__main__':
    unittest.main()
