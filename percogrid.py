"""
a percolation system is represented using a grid of sites.
Each site is either OPENED or BLOCKED. A full site is an OPENED site that can
be connected to an OPENED site in the top row via a chain of neighboring
OPENED sites.

We say the system percolates if there is a full site in the bottom row.
In other words, a system percolates if we fill all OPENED sites connected
to the top row and that process fills some OPENED site on the bottom row
"""

from congeries import WeightedQuickUnionPathCompressionUF
from enum import Enum


class Site(Enum):
    """a Site is either OPENED or BLOCKED
    """
    BLOCKED = 0
    OPENED = 1

    def __str__(self):
        if self is self.BLOCKED:
            return '\u2588'
        else:
            return ' '


class PercoGrid:
    """
    uses an n-by-n grid of sites to represent a percolation model
    neighbors are left, right, up, and down

    By convention, the row and column indices are integers between
    1 and n, where (1, 1) is the upper-left site
    """

    neighbor_offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, n: int) -> None:
        """creates n-by-n grid, with all sites initially BLOCKED

        :param n: int, number of sites in a side of the square grid
        """
        if n <= 0:
            raise ValueError('n must be > 0')
        self.rows = self.cols = n
        self.size = self.rows * self.cols
        self.grid = [[Site.BLOCKED for col in range(n)] for row in range(n)]
        self.number_open_sites = 0
        self.uf = WeightedQuickUnionPathCompressionUF(self.size+2)
        self.top_ndx, self.bot_ndx = self.size, self.size + 1
        self._connect_top_and_bottom()

    def _connect_top_and_bottom(self):
        print(self.uf.components_count)
        for idx in range(self.cols):
            self.uf.union(self.top_ndx, idx)
            print(self.uf.components_count)
        for idx in range(self.rows * (self.cols - 1), self.size):
            self.uf.union(self.bot_ndx, idx)
            print(self.uf.components_count)

    def _base_1_to_base_0(self, row, col):
        if not self._is_valid_row(row):
            raise ValueError('row must be >= 1 and <= {self.rows}')
        if not self._is_valid_col(col):
            raise ValueError('col must be >= 1 and <= {self.cols}')
        return row - 1, col - 1

    def _is_valid_row(self, row: int) -> bool:
        return 1 <= row <= self.rows

    def _is_valid_col(self, col: int) -> bool:
        return 1 <= col <= self.cols

    def open(self, row: int, col: int) -> None:
        """opens the site (row, col) if it is not OPENED already

        :param row: int, the row
        :param col: col, the col
        :return: None
        """
        r, c = self._base_1_to_base_0(row, col)
        if self.grid[r][c] != Site.OPENED:
            self.grid[r][c] = Site.OPENED
            self.number_open_sites += 1

    def isopen(self, row: int, col: int) -> bool:
        """is the site at pos (row, col) OPENED?

        :param row: int, the row
        :param col: col, the col
        :return: True if the site is OPENED, False otherwise
        """
        r, c = self._base_1_to_base_0(row, col)
        return self.grid[r][c] == Site.OPENED

    def __str__(self):
        result = []
        for row in self.grid:
            result.append(''.join((str(site) for site in row)))
        return '\n'.join(result)


if __name__ == '__main__':

    pg = PercoGrid(6)
    # pg.open(1, 1)
    print(pg)