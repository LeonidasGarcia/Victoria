import tkinter as tk
from tkinter import Frame

class ProgramForm(Frame):
    def __init__(self, master, **kwargs):
        self.program_count = 0

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        tk.Label(self, text="Programas").grid(row=0, column=0, sticky=tk.W)

        tk.Label(self, text="Número de programas").grid(row=1, column=0, sticky=tk.W)
        self.program_count_input = tk.Entry(self)
        self.program_count_input.grid(row=1, column=1, sticky=tk.NSEW)