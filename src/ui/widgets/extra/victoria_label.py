import tkinter as tk
from tkinter import Frame

from src.ui.colors import victoria_background


class VictoriaLabel(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_propagate(False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(7, weight=1)
        self.rowconfigure(0, weight=1)

        v = tk.Label(self, text="V", bg=victoria_background)
        v.grid(row=0, column=0, sticky="nse")
        i = tk.Label(self, text="i", bg=victoria_background)
        i.grid(row=0, column=1, sticky="nsew")
        c = tk.Label(self, text="c", bg=victoria_background)
        c.grid(row=0, column=2, sticky="nsew")
        t = tk.Label(self, text="t", bg=victoria_background)
        t.grid(row=0, column=3, sticky="nsew")
        o = tk.Label(self, text="o", bg=victoria_background)
        o.grid(row=0, column=4, sticky="nsew")
        r = tk.Label(self, text="r", bg=victoria_background)
        r.grid(row=0, column=5, sticky="nsew")
        i = tk.Label(self, text="i", bg=victoria_background)
        i.grid(row=0, column=6, sticky="nsew")
        a = tk.Label(self, text="a", bg=victoria_background)
        a.grid(row=0, column=7, sticky="nsw")