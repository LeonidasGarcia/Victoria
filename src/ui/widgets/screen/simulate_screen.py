import tkinter as tk
from tkinter import Frame
from typing import List

from src.core.victoria import Victoria
from src.ui.widgets.core.victoria_cell import VictoriaCell
from src.ui.widgets.form.models.reference_trace_model import ReferenceTraceModel
from src.util.lib import gen_hex_colors_list


class SimulateScreen(Frame):
    def __init__(self, master, victoria_units: List[Victoria], program_count: int, reference_trace: List[ReferenceTraceModel], **kwargs):
        self.victoria_units: List[Victoria] = victoria_units
        self.victoria_cells: dict[int, VictoriaCell] = {}
        self.program_count: int = program_count
        self.program_colors: List[str] = gen_hex_colors_list(quantity=program_count)
        self.reference_trace: List[ReferenceTraceModel] = reference_trace
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

        self.play_button = tk.Button(buttons_frame, text="Play", command=self.resume_cells)
        self.play_button.grid(row=0, column=0, sticky="nsew")

        self.pause_button = tk.Button(buttons_frame, text="Pause", command=self.stop_cells)
        self.pause_button.grid(row=0, column=1, sticky="nsew")

        self.reset_button = tk.Button(buttons_frame, text="Reset", command=self.reset_cells)
        self.reset_button.grid(row=0, column=2, sticky="nsew")

        self.cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.master.load_form_screen())
        self.cancel_button.grid(row=0, column=3, sticky="nsew")

        self.controls_frame.grid(row=1, column=0, sticky="nsew")

    def stop_cells(self):
        for cell in self.victoria_cells.values():
            cell.stop_current_request()

    def resume_cells(self):
        for cell in self.victoria_cells.values():
            cell.resume_current_request()

    def reset_cells(self):
        for cell in self.victoria_cells.values():
            cell.reset_current_request()

    def cells_frame_setup(self):
        cells_frame = self.cells_frame

        for i in range(0, self.units_count):
            cells_frame.grid_columnconfigure(i, weight=1)

        cells_frame.grid_rowconfigure(0, weight=1)

        for i, victoria in enumerate(self.victoria_units):
            victoria_cell = VictoriaCell(cells_frame, victoria=victoria, program_count=self.program_count, program_colors=self.program_colors, reference_trace=self.reference_trace)
            victoria_cell.grid(row=0, column=i, sticky="nsew")
            self.victoria_cells[i] = victoria_cell

    def stop_simulation(self):
        for cell in self.victoria_cells.values():
            cell.stop_current_request()