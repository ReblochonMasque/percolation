import unittest

from visualizer import val_closest_to


class TestVisualizer(unittest.TestCase):

    def test_val_closest_to_0(self):
        expected = 99
        actual = val_closest_to(11, 100)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
