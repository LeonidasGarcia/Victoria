import tkinter as tk
from tkinter import Frame

from src.ui.colors import victoria_background
from src.util.svg_conversor import load_svg_icon, load_jpeg_icon


class VictoriaLabel(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.svg_icon = load_jpeg_icon("../assets/victoria_logo.png", (350, 50))
        self.icon_label = tk.Label(self, bg=victoria_background, width=100, image=self.svg_icon)
        self.icon_label.grid(row=0, column=0, sticky="nsew")
