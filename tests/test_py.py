import unittest


class TestPy(unittest.TestCase):

    def test_false(self):
        # 🤔
        self.assertFalse(0)
        self.assertFalse(0.0)
        self.assertFalse([])
        self.assertFalse(())
        self.assertFalse({})


if __name__ == '__main__':
    unittest.main()
