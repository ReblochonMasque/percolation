import time
import tkinter as tk

from percogrid import PercoGrid
from typing import MutableMapping, Tuple


# class UFView(tk.Canvas):
#
#     def __init__(self, master, n: int = 10, scale: int = 1):
#         super().__init__(master)
#         self.master = master
#         self.n = n


class PercoView(tk.Canvas):
    left_offset = 3
    top_offset = 3
    states = ['black', 'white', 'blue']

    def __init__(self, master, n: int, site_size: int):
        super().__init__(master)
        self.master = master
        self.n = n
        self.site_size = site_size
        self.site_cells: MutableMapping[Tuple[int, int], int] = {}
        self.create_grid()

    def create_grid(self):
        for row in range(self.n):
            for col in range(self.n):
                self.site_cells[(row, col)] = \
                    self.create_rectangle(
                        *self._get_coords(row, col),
                        outline='grey20',
                        fill=self.states[0],
                    )

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
        for r, line in enumerate(pg.grid):
            for c, site in enumerate(line):
                status = site.value
                if status == 1 and pg.isfull(r+1, c+1):
                    status = 2
                self.update_site(r, c, status)

    def update_site(self, row, col, status):
        self.itemconfig(self.site_cells[(row, col)], fill=self.states[status])


def run(pg, pv, sites):
    site = sites.pop(0)
    pg.open(*site)
    pv.update_sites(pg)
    root.after(500, run, pg, pv, sites)



if __name__ == '__main__':

    WIDTH = HEIGHT = 600

    sites = [(1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (5, 5), (1, 2)]

    root = tk.Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}+100+100')
    n = 5
    pv = PercoView(root, n, (WIDTH-PercoView.left_offset*2)//n)
    pv.pack(expand=True, fill=tk.BOTH)

    pg = PercoGrid(n)

    tk.Button(root, text='run', command=lambda: run(pg, pv, sites)).pack()

    root.mainloop()
