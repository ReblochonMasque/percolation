
import tkinter as tk


class UFView(tk.Canvas):

    def __init__(self, master, n: int = 10, scale: int = 1):
        super().__init__(master)
        self.master = master
        self.n = n


class PercoView(tk.Canvas):

    def __init__(self, master, n: int = 10, scale: int = 1):
        super().__init__(master)
        self.master = master
        self.n = n


if __name__ == '__main__':

    root = tk.Tk()
    pv = PercoView(root)
    pv.pack()

    root.mainloop()