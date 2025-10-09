import tkinter as tk
from tkinter import Frame, ttk
from typing import Optional

from src.ui.widgets.form.algorithm_form import AlgorithmForm
from src.ui.widgets.form.memory_form import MemoryForm
from src.ui.widgets.form.program_form import ProgramForm
from src.ui.widgets.form.reference_trace_form import ReferenceTraceForm


class FormScreen(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.presets_combobox = ttk.Combobox(self, values=[])
        self.presets_combobox.grid(row=0, column=0, sticky="w")

        self.memory_form = MemoryForm(self, bg="red")
        self.memory_form.grid(row=1, column=0, sticky=tk.NSEW)

        self.algorithm_form = AlgorithmForm(self)
        self.algorithm_form.grid(row=2, column=0, sticky=tk.NSEW)

        self.program_form = ProgramForm(self)
        self.program_form.grid(row=0, column=1, sticky=tk.NSEW)

        self.reference_trace = ReferenceTraceForm(self)
        self.reference_trace.grid(row=1, rowspan=2, column=1, sticky=tk.NSEW)

        self.start_frame = tk.Frame(self)

        self.start_frame.grid_columnconfigure(0, weight=1)
        self.start_frame.grid_rowconfigure(0, weight=1)
        self.start_frame.grid_rowconfigure(1, weight=1)

        self.start_frame.grid(row=0, rowspan=3, column=2, sticky=tk.NSEW)

        self.save_button = tk.Button(self.start_frame, text="Guardar como preset")
        self.save_button.grid(row=0, column=0, sticky=tk.S)

        self.start_button = tk.Button(self.start_frame, text="Iniciar")
        self.start_button.grid(row=1, column=0, sticky=tk.N)
