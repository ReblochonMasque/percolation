
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


if __name__ == '__main__':

    root = tk.Tk()
    pv = PercoView(root)
    pv.pack()

    root.mainloop()