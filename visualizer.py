
import tkinter as tk


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