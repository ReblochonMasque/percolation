import tkinter as tk

from percolation import Percolation
from typing import MutableMapping, Tuple


class PercolationGridView(tk.Canvas):

    left_offset = 3
    top_offset = 3
    states = ['black', 'white', 'blue']

    def __init__(self, master, n: int, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.n = n
        self.site_size = kwargs['width'] // self.n
        self.site_cells: MutableMapping[Tuple[int, int], int] = {}
        self.reverse_site_cells: MutableMapping[int, Tuple[int, int]] = {}
        self.create_grid()

        self.bind("<Button-1>", self.open)

    def open(self, event):
        print(self.find_closest(event.x, event.y))
        print(self.reverse_site_cells[self.find_closest(event.x, event.y)[0]])
        pg.open(*self.reverse_site_cells[self.find_closest(event.x, event.y)[0]])
        self.update_sites(pg)
        print(f'components_count: {pg.uf_top.components_count}')

    def create_grid(self):
        for row in range(self.n):
            for col in range(self.n):
                site = self.create_rectangle(
                    *self._get_coords(row, col),
                    outline='grey20',
                    fill=self.states[0],
                )
                self.site_cells[(row, col)] = site
                self.reverse_site_cells[site] = (row+1, col+1)

    def _get_coords(
            self,
            row,
            col
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        x0 = col * self.site_size + self.left_offset
        y0 = row * self.site_size + self.top_offset
        x1, y1 = x0 + self.site_size, y0 + self.site_size
        return (x0, y0), (x1, y1)

    def update_sites(self, pg):
        for sdx in range(1, pg.size+1):
            row, col = (sdx-1) // pg.rows + 1, (sdx-1) % pg.cols + 1
            status = 0
            if pg.isfull(row, col):
                status = 2
            elif pg.isopen(row, col):
                status = 1
            self.update_site(row-1, col-1, status)

    def update_site(self, row, col, status):
        self.itemconfig(self.site_cells[(row, col)], fill=self.states[status])


class PercoFrame(tk.Frame):
    _grid_width, _grid_height = 600, 600

    def __init__(self, master, n: int):
        self.master = master
        super().__init__(self.master)
        self.n = n
        _gw = _gh = val_closest_to(self.n, PercoFrame._grid_width)
        self.grid_width = _gw + PercolationGridView.left_offset * 2
        self._grid_height = _gh + PercolationGridView.top_offset * 2
        self.percocanvas = PercolationGridView(self, n, width=self.grid_width, height=self._grid_height)
        self.percocanvas.pack()


class Controller:

    def __init__(self, n: int):
        self.n = n
        self.perco = Percolation(self.n)
        self.master = tk.Tk()
        self.percoframe = PercoFrame(self.master, self.n)
        self.percoframe.pack()


def val_closest_to(n: int, val: int) -> int:
    """returns the integer value closest to val that can be divided into n int partitions

    :param n: int, number of partitions
    :param val: int, value to approximate
    :return: int, approximate value closest to val
    """
    n_partitions = val // n
    low, high = val - n_partitions * n, n * (n_partitions + 1) - val
    if low < high:
        return n_partitions * n
    return (n_partitions + 1) * n


# def run(pg, pv, sites):
#     site = sites.pop(0)
#     pg.open(*site)
#     pv.update_sites(pg)
#     root.after(500, run, pg, pv, sites)


if __name__ == '__main__':

    # sites = [(1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (5, 5), (1, 2)]
    #
    # root = tk.Tk()
    # root.geometry(f'{WIDTH}x{HEIGHT}+100+100')
    # n = 5
    # pv = PercolationGridView(root, n, (WIDTH - PercolationGridView.left_offset * 2) // n)
    # pv.pack(expand=True, fill=tk.BOTH)
    #
    # pg = Percolation(n)
    #
    # tk.Button(root, text='run', command=lambda: run(pg, pv, sites)).pack()

    c = Controller(10)

    c.master.mainloop()
