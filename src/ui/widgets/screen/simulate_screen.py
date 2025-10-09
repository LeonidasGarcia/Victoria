import tkinter as tk
from tkinter import Frame
from typing import List

from src.core.victoria import Victoria
from src.ui.widgets.core.victoria_cell import VictoriaCell


class SimulateScreen(Frame):
    def __init__(self, master, victoria_units: List[Victoria], **kwargs):
        self.victoria_units: List[Victoria] = victoria_units
        self.victoria_cells: dict[int, VictoriaCell] = {}
        self.units_count = len(victoria_units)

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)

        self.cells_frame = tk.Frame(self)
        self.cells_frame_setup()
        self.cells_frame.grid(row=0, column=0, sticky="nsew")

        self.controls_frame = tk.Frame(self)
        self.controls_frame_setup()
        self.controls_frame.grid(row=1, column=0, sticky="nsew")


    def cells_frame_setup(self):
        cells_frame = self.cells_frame

        for i in range(0, self.units_count):
            cells_frame.grid_columnconfigure(i, weight=1)

        cells_frame.grid_rowconfigure(0, weight=1)

        for i, victoria in enumerate(self.victoria_units):
            victoria_cell = VictoriaCell(cells_frame, victoria=victoria)
            victoria_cell.grid(row=0, column=i, sticky="nsew")
            self.victoria_cells[i] = victoria_cell

    def controls_frame_setup(self):
        controls_frame = self.controls_frame

        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=9)
        controls_frame.grid_rowconfigure(0, weight=1)

        spacer = tk.Frame(controls_frame)
        spacer.grid(row=0, column=1, sticky="nsew")

        buttons_frame = tk.Frame(controls_frame, bg="red")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame.grid_columnconfigure(3, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid(row=0, column=0, sticky="nsew")

        play_button = tk.Button(buttons_frame, text="Play")
        play_button.grid(row=0, column=0, sticky="nsew")

        pause_button = tk.Button(buttons_frame, text="Pause")
        pause_button.grid(row=0, column=1, sticky="nsew")

        reset_button = tk.Button(buttons_frame, text="Reset")
        reset_button.grid(row=0, column=2, sticky="nsew")

        cancel_button = tk.Button(buttons_frame, text="Cancel")
        cancel_button.grid(row=0, column=3, sticky="nsew")