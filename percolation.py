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
from typing import List


class Percolation:
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
        self.opened_site = set()
        self.uf_top = WeightedQuickUnionPathCompressionUF(self.size+2)
        self.uf_bot = WeightedQuickUnionPathCompressionUF(self.size+2)
        self.virtual_top, self.virtual_bot = self.size, self.size + 1
        self._percolates = False

    def _is_valid_row_col(self, row: int, col: int) -> bool:
        return 1 <= row <= self.rows and 1 <= col <= self.cols

    def _get_flat_index(self, row: int, col: int) -> int:
        return (row - 1) * self.cols + col - 1

    def _get_flat_neighbors(self, row: int, col: int) -> List[int]:
        neighbors = []
        for dr, dc in self.neighbor_offsets:
            nr, nc = row + dr, col + dc
            if self._is_valid_row_col(nr, nc):
                neighbors.append(self._get_flat_index(nr, nc))
        return neighbors

    def open(self, row: int, col: int) -> None:
        site = self._get_flat_index(row, col)
        if site in self.opened_site:
            return
        self.opened_site.add(site)
        for neighbor in self._get_flat_neighbors(row, col):
            if neighbor in self.opened_site:
                self.uf_top.union(site, neighbor)
                self.uf_bot.union(site, neighbor)
        if row == 1:
            self.uf_top.union(site, self.virtual_top)
        if row == self.rows:
            self.uf_bot.union(site, self.virtual_bot)
        if self.uf_top.connected(site, self.virtual_top) and \
                self.uf_bot.connected(site, self.virtual_bot):
            self._percolates = True

    def isopen(self, row: int, col: int) -> bool:
        return self._get_flat_index(row, col) in self.opened_site

    def isfull(self, row, col):
        return self.uf_top.connected(self._get_flat_index(row, col), self.virtual_top)

    def percolates(self) -> bool:
        return self._percolates

    def __str__(self):
        res = []
        for row in range(1, self.rows+1):
            for col in range(1, self.cols+1):
                c = '█'
                if self.isopen(row, col):
                    c = ' '
                if self.isfull(row, col):
                    c = '.'
                res.append(c)
            res.append('\n')
        return ''.join(res)


if __name__ == '__main__':

    sites = [(5, 1), (4, 1), (3, 1), (5, 3), (1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (5, 5), (1, 2)]
    n = 5
    pg = Percolation(n)
    for row, col in sites:
        pg.open(row, col)
        print(row, col)
        input()
        print(pg)
        if pg.percolates():
            print('PERCOLATES!!')
            break
    print(pg)
