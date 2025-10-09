import tkinter as tk
from tkinter import Frame

class MemoryForm(Frame):
    def __init__(self, master, **kwargs):
        self.ram: int = 0
        self.program_size: int = 0
        self.page_size: int = 0

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_label = tk.Label(self, text="Memoria")
        title_label.grid(row=0, column=0, columnspan=2, sticky="w")

        inputs_frame = tk.Frame(self, bg="yellow")

        inputs_frame.grid_columnconfigure(0, weight=1)
        inputs_frame.grid_columnconfigure(1, weight=1)
        inputs_frame.grid_rowconfigure(0, weight=1)
        inputs_frame.grid_rowconfigure(1, weight=1)
        inputs_frame.grid_rowconfigure(2, weight=1)

        inputs_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        tk.Label(inputs_frame, text="RAM").grid(row=0, column=0, sticky="w")
        self.ram_input = tk.Entry(inputs_frame)
        self.ram_input.grid(row=0, column=1, sticky="nsew")

        tk.Label(inputs_frame, text="Tamaño del programa").grid(row=1, column=0, sticky="w")
        self.program_size_input = tk.Entry(inputs_frame)
        self.program_size_input.grid(row=1, column=1, sticky="nsew")

        tk.Label(inputs_frame, text="Tamaño de página").grid(row=2, column=0, sticky="w")
        self.page_size_input = tk.Entry(inputs_frame)
        self.page_size_input.grid(row=2, column=1, sticky="nsew")