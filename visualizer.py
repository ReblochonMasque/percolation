import tkinter as tk

from congeries import WeightedQuickUnionPathCompressionUF
from percolation import Percolation
from typing import MutableMapping, Tuple

from pubsub import pub


class PercolationGridView(tk.Canvas):

    lr_offset = 20
    tb_offset = 20
    states = ['black', 'white', 'blue']

    def __init__(self, master, n: int, width: int = 0, height: int = 0):
        full_width, full_height = width + 2 * self.lr_offset, height + 2 * self.tb_offset
        super().__init__(master, width=full_width, height=full_height, bg='cyan')
        self.master = master
        self.n = n
        self.site_size = width // self.n
        self.site_cells: MutableMapping[Tuple[int, int], int] = {}
        self.reverse_site_cells: MutableMapping[int, Tuple[int, int]] = {}
        self.create_grid()

        self.bind("<Button-1>", self.on_click)

        pub.subscribe(self.update_sites, "update_view")

    def on_click(self, event):
        row, col = self.reverse_site_cells[self.find_closest(event.x, event.y)[0]]
        pub.sendMessage("open_site", row=row, col=col)

    def create_grid(self):
        for row in range(self.n):
            for col in range(self.n):
                site = self.create_rectangle(
                    *self._get_rectangle_coords(row, col),
                    outline='grey20',
                    fill=self.states[0],
                )
                self.site_cells[(row, col)] = site
                self.reverse_site_cells[site] = (row+1, col+1)

    def _get_rectangle_coords(
            self,
            row,
            col
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        x0 = col * self.site_size + self.lr_offset
        y0 = row * self.site_size + self.tb_offset
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

    def __init__(self, master, controller, n: int):
        self.master = master
        super().__init__(self.master)
        self.controller = controller
        self.n = n
        _gw = _gh = val_closest_to(self.n, PercoFrame._grid_width)
        self.grid_width, self._grid_height = _gw, _gh
        self.percocanvas = PercolationGridView(self, n, width=self.grid_width, height=self._grid_height)
        self.percocanvas.pack()

        self.dashboard = tk.Frame(self)

        self.left_dash = tk.Frame(self)
        self.open_sites_var = tk.StringVar()
        self.display_open_sites_lbl = tk.Label(self.left_dash, textvariable=self.open_sites_var)
        self.display_open_sites_lbl.pack(anchor=tk.NE)

        self.connected_components_var = tk.StringVar()
        self.display_connected_components_lbl = tk.Label(self.left_dash, textvariable=self.connected_components_var)
        self.display_connected_components_lbl.pack(anchor=tk.NE)
        self.left_dash.pack(side=tk.LEFT)

        self.percolates_var = tk.StringVar()
        self.display_percolates_var_lbl = tk.Label(self.dashboard, textvariable=self.percolates_var)
        self.display_percolates_var_lbl.pack(side=tk.RIGHT)

        self.dashboard.pack(fill=tk.X)

        pub.subscribe(self.update_data, "update_data")

    def update_data(self, open_sites: int, conn_components: int, percolates: bool) -> None:
        self.open_sites_var.set(f'open sites: {open_sites}')
        self.connected_components_var.set(f'connected_components: {conn_components}')
        self.percolates_var.set(f'percolates: {percolates}')


class Controller:

    def __init__(self, n: int):
        self.n = n
        self.perco = Percolation(self.n)
        self.uf = WeightedQuickUnionPathCompressionUF(self.n)
        self.master = tk.Tk()
        self.percoframe = PercoFrame(self.master, self, self.n)
        self.percoframe.pack()

        self.dispatch_messages()

        pub.subscribe(self.open_site, "open_site")

    def open_site(self, row: int, col: int) -> None:
        """receives instructions from interactive canvas to open a site in the model

        calls for sending a message with the updated model state
        :param row: int
        :param col: int
        :return: None
        """
        self.perco.open(row, col)
        self.dispatch_messages()

    def dispatch_messages(self) -> None:
        """publishes messages when the status of the model changes

        :return: None
        """
        pub.sendMessage("update_view", pg=self.perco)
        open_sites = self.perco.number_of_open_sites()
        conn_components = self.perco.uf_top.components_count, self.perco.uf_bot.components_count
        percolates = self.perco.percolates()
        pub.sendMessage("update_data",
                        open_sites=open_sites,
                        conn_components=conn_components,
                        percolates=percolates)


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

    n = 15
    controller = Controller(n)

    controller.master.mainloop()
