
import tkinter as tk

from typing import Any, Mapping, Tuple


class UFView(tk.Canvas):

    def __init__(self, master, n: int = 10, scale: int = 1):
        super().__init__(master)
        self.master = master
        self.n = n


class PercoView(tk.Canvas):
    left_offset = 3
    top_offset = 3

    def __init__(self, master, n: int = 10, site_size: int = 25):
        super().__init__(master)
        self.master = master
        self.n = n
        self.site_size = site_size
        self.sites: Mapping[Tuple[int, int], int] = {}

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

    root = tk.Tk()
    pv = PercoView(root)
    pv.pack()

    root.mainloop()