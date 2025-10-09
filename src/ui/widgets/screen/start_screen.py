import tkinter as tk
from tkinter import Frame

from src.core.algorithms.clk import Clk
from src.core.victoria import Victoria
from src.ui.colors import victoria_background
from src.ui.widgets.core.victoria_cell import VictoriaCell
from src.util.metrics import Metrics


class StartScreen(Frame):
    def __init__(self, master, **kwargs):
        self.sample = None

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(self, bg=victoria_background)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self, bg=victoria_background)
        self.right_frame_setup()

    def left_frame_setup(self):
        pass

    def right_frame_setup(self):
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

        self.right_frame.grid(row=0, column=1, sticky="nsew")

        sample = VictoriaCell(self.right_frame, victoria=Victoria(pra=Clk(), metrics=Metrics(), ram=204800, program_size=24576, page_size=4096), bg=victoria_background)
        sample.grid(row=0, column=0, sticky="nsew")

        self.sample = sample