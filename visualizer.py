
import tkinter as tk


class UFView(tk.Canvas):

    def __init__(self, master, n: int, scale: int):
        super().__init__(master)
        self.master = master
        self.n = n


class PercoView(tk.Canvas):

    def __init__(self, master, n: int, scale: int):
        super().__init__(master)
        self.master = master
        self.n = n


if __name__ == '__main__':

    pg = PercoGrid(6)
    while True:
        r = input('row:')
        c = input('col:')
        pg.open(int(r), int(c))
        print(pg)
        print(pg.uf.id)
        if pg.percolates():
            print('PERCOLATES!')
            break

    print('done!')