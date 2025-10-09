import tkinter as tk
from tkinter import Toplevel, ttk

from src.ui.widgets.form.memory_form import MemoryForm
from src.ui.widgets.form.program_form import ProgramForm
from src.ui.widgets.form.reference_trace_form import ReferenceTraceForm


class Presets(Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Presets")
        self.geometry("450x600")
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=20)

        self.controls_frame = tk.Frame(self)

        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, weight=1)
        self.controls_frame.grid_columnconfigure(3, weight=1)
        self.controls_frame.grid_columnconfigure(4, weight=1)
        self.controls_frame.grid_rowconfigure(0, weight=1)

        self.controls_frame.grid(row=0, column=0, sticky="nsew")

        self.presets_combobox = ttk.Combobox(self.controls_frame, state="readonly")
        self.presets_combobox.grid(row=0, column=0, sticky="nsew")

        self.save_button = tk.Button(self.controls_frame, text="Guardar")
        self.save_button.grid(row=0, column=1, sticky="nsew")

        self.reset_button = tk.Button(self.controls_frame, text="Reset")
        self.reset_button.grid(row=0, column=2, sticky="nsew")

        self.delete_button = tk.Button(self.controls_frame, text="Delete")
        self.delete_button.grid(row=0, column=3, sticky="nsew")

        self.memory_form = MemoryForm(self, bg="red")
        self.memory_form.grid(row=1, column=0, sticky=tk.NSEW)

        self.program_form = ProgramForm(self)
        self.program_form.grid(row=2, column=0, sticky=tk.NSEW)

        self.reference_trace = ReferenceTraceForm(self)
        self.reference_trace.grid(row=3, column=0, sticky=tk.NSEW)