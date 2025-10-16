import tkinter as tk
from tkinter import Frame

from src.core.algorithms.clk import Clk
from src.core.algorithms.lru import Lru
from src.core.constants import welcome_message
from src.core.victoria import Victoria
from src.ui.colors import victoria_background
from src.ui.widgets.core.victoria_cell import VictoriaCell
from src.ui.widgets.form.models.memory_model import MemoryModel
from src.ui.widgets.form.models.program_model import ProgramModel
from src.ui.widgets.form.models.reference_trace_model import ReferenceTraceModel
from src.util.lib import gen_hex_colors_list
from src.util.metrics import Metrics


class StartScreen(Frame):
    def __init__(self, master, **kwargs):
        self.sample = None

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(self, bg=victoria_background)
        self.left_frame_setup()
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self, bg=victoria_background)
        self.right_frame_setup()
        self.right_frame.grid(row=0, column=1, sticky="nsew")

    def left_frame_setup(self):
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)

        tk.Label(self.left_frame, bg=victoria_background,
                 justify="left",
                 wraplength=600,
                 text=welcome_message,
                 fg="white").grid(row=0, column=0, sticky="ns")

    def right_frame_setup(self):
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

        sample = VictoriaCell(
            self.right_frame,
            victoria=Victoria(ram=102400, program_size=204800, page_size=4096, pra=Lru(), metrics=Metrics()),
            program_count=5,
            program_colors=gen_hex_colors_list(quantity=5),
            bg=victoria_background
        )
        sample.grid(row=0, column=0, sticky="nsew")

        self.sample = sample
