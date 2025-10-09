import tkinter as tk
from tkinter import Frame, ttk
from typing import Tuple, List


class ReferenceTraceForm(Frame):
    def __init__(self, master, **kwargs):
        self.reference_trace: List[Tuple[int, int, str]] = []

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

        tk.Label(self, text="Rastreo de referencias").grid(row=0, column=0, columnspan=2, sticky=tk.W)

        tk.Label(self, text="PID").grid(row=1, column=0, sticky=tk.W)
        self.pid_input = tk.Entry(self)
        self.pid_input.grid(row=1, column=1)

        tk.Label(self, text="Número de página").grid(row=2, column=0, sticky=tk.W)
        self.num_page_input = tk.Entry(self)
        self.num_page_input.grid(row=2, column=1)

        tk.Label(self, text="Modo").grid(row=3, column=0, sticky=tk.W)
        self.mode_input = tk.Entry(self)
        self.mode_input.grid(row=3, column=1)

        self.register_button = tk.Button(self, text="Registrar")
        self.register_button.grid(row=4, column=0, columnspan=2)

        self.reference_trace_table = ttk.Treeview(self)
        self.reference_trace_table.grid(row=1, rowspan=4, column=2, columnspan=2, sticky=tk.NSEW)

        self.delete_reference_button = tk.Button(self, text="Eliminar")
        self.delete_reference_button.grid(row=5, column=3, sticky=tk.NSEW)