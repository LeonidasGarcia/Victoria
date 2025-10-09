import tkinter as tk
from tkinter import Frame

from src.ui.colors import victoria_background


class Navigator(Frame):
    def __init__(self, master, **kwargs):
        self.navigation_label = None

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        navigation_label = tk.Label(self, text="Inicio", bg=victoria_background)
        navigation_label.grid(row=0, column=0, sticky="nsw")

        self.navigation_label = navigation_label