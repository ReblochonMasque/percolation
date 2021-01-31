import io
import unittest

from contextlib import redirect_stdout
from percogrid import PercoGrid


class TestPercoGrid(unittest.TestCase):

    def test_type(self):
        pg = PercoGrid(6)
        self.assertIsInstance(pg, PercoGrid)

    def test_n_equal_0(self):
        with self.assertRaises(ValueError):
            pg = PercoGrid(0)

    def test_n_equal_minus_100(self):
        with self.assertRaises(ValueError) as e:
            pg = PercoGrid(-100)

    def test_str_0(self):
        pg = PercoGrid(4)
        actual = io.StringIO()
        with redirect_stdout(actual):
            print(pg)
        expected = "████\n████\n████\n████\n"
        self.assertEqual(expected, actual.getvalue())

    def test_str_1(self):
        pg = PercoGrid(4)
        pg.open(1, 1)
        actual = io.StringIO()
        with redirect_stdout(actual):
            print(pg)
        expected = " ███\n████\n████\n████\n"
        self.assertEqual(expected, actual.getvalue())

    def test_str_2(self):
        pg = PercoGrid(4)
        for row, col in ((1, 1), (2, 2), (3, 3), (4, 4), (4, 1), (3, 2), (2, 3), (1, 4)):
            pg.open(row, col)
        actual = io.StringIO()
        with redirect_stdout(actual):
            print(pg)
        expected = " ██ \n█  █\n█  █\n ██ \n"
        self.assertEqual(expected, actual.getvalue())

    def test_isopen_not(self):
        pg = PercoGrid(4)
        self.assertFalse(pg.isopen(1, 1))

    def test_open_valid_site(self):
        pg = PercoGrid(4)
        pg.open(1, 2)
        self.assertTrue(pg.isopen(1, 2))

    def test_number_open_sites_0(self):
        pg = PercoGrid(4)
        expected, actual = 0, pg.number_open_sites
        self.assertEqual(expected, actual)

    def test_number_open_sites_2_b(self):
        pg = PercoGrid(4)
        pg.open(1, 2)
        pg.open(1, 2)
        pg.open(2, 2)
        expected, actual = 2, pg.number_open_sites
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
