"""
a percolation system is represented using a grid of sites.
Each site is either open or blocked. A full site is an open site that can
be connected to an open site in the top row via a chain of neighboring
open sites.

We say the system percolates if there is a full site in the bottom row.
In other words, a system percolates if we fill all open sites connected
to the top row and that process fills some open site on the bottom row
"""

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
    """

    neighbor_offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, n: int) -> None:
        """creates n-by-n grid, with all sites initially blocked

        :param n: int, number of sites in a side of the square grid
        """
        self.size = n * n
        self.grid = [[Site.blocked for col in range(n)] for row in range(n)]

    def __str__(self):
        res = []
        for row in self.grid:
            for site in row:
                if site is Site.blocked:
                    res.append('X')
                else:
                    res.append(' ')
            res.append('\n')
        return ''.join(res)


if __name__ == '__main__':

    pg = PercoGrid(6)
    print(pg)