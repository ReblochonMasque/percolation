
import tkinter as tk

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
                        fill='black',
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


if __name__ == '__main__':

    WIDTH = HEIGHT = 600

    root = tk.Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}+100+100')
    n = 25
    pv = PercoView(root, n, (WIDTH-PercoView.left_offset*2)//n)
    pv.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
