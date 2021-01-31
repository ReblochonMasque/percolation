"""
a percolation system is represented using a grid of sites.
Each site is either open or blocked. A full site is an open site that can
be connected to an open site in the top row via a chain of neighboring
open sites.

We say the system percolates if there is a full site in the bottom row.
In other words, a system percolates if we fill all open sites connected
to the top row and that process fills some open site on the bottom row
"""

from congeries import WeightedQuickUnionPathCompressionUF
from enum import Enum


class Site(Enum):
    """a Site is either open or blocked
    """
    blocked = 0
    open = 1


class PercoGrid:
    """
    uses an n-by-n grid of sites to represent a percolation model
    neighbors are left, right, up, and down

    By convention, the row and column indices are integers between
    1 and n, where (1, 1) is the upper-left site
    """

    neighbor_offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, n: int) -> None:
        """creates n-by-n grid, with all sites initially blocked

        :param n: int, number of sites in a side of the square grid
        """
        if n <= 0:
            raise ValueError('n must be > 0')
        self.size = n * n
        self.grid = [[Site.blocked for col in range(n)] for row in range(n)]
        self.uf = WeightedQuickUnionPathCompressionUF(self.size)

    def open(self, row: int, col: int) -> None:
        """opens the site (row, col) if it is not open already

        :param row: int, the row
        :param col: col, the col
        :return: None
        """
        if self.grid[row][col] != Site.open:
            self.grid[row][col] = Site.open

    def isopen(self, row: int, col: int) -> bool:
        """is the site at pos (row, col) open?

        :param row: int, the row
        :param col: col, the col
        :return: True if the site is open, False otherwise
        """
        return self.grid[row][col] == Site.open

    def __str__(self):
        result = []
        for row in self.grid:
            res = []
            for site in row:
                val = ' '
                if site is Site.blocked:
                    val = 'X'
                res.append(val)
            result.append(''.join(res))
        return '\n'.join(result)


if __name__ == '__main__':

    pg = PercoGrid(6)
    print(pg)