import tkinter as tk
from statistics import variance
from tkinter import Frame
from typing import Optional

from pydantic import ValidationError

from src.ui.widgets.form.models.memory_model import MemoryModel


class MemoryForm(Frame):
    def __init__(self, master, **kwargs):
        self.memory_model: Optional[MemoryModel] = None

        self.ram: int = 0
        self.program_size: int = 0
        self.page_size: int = 0

        self.ram_string_var = tk.StringVar()
        self.program_size_string_var = tk.StringVar()
        self.page_size_string_var = tk.StringVar()

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
        self.ram_input = tk.Entry(inputs_frame, textvariable=self.ram_string_var)
        self.ram_input.grid(row=0, column=1, sticky="nsew")

        tk.Label(inputs_frame, text="Tamaño del programa").grid(row=1, column=0, sticky="w")
        self.program_size_input = tk.Entry(inputs_frame, textvariable=self.program_size_string_var)
        self.program_size_input.grid(row=1, column=1, sticky="nsew")

        tk.Label(inputs_frame, text="Tamaño de página").grid(row=2, column=0, sticky="w")
        self.page_size_input = tk.Entry(inputs_frame, textvariable=self.page_size_string_var)
        self.page_size_input.grid(row=2, column=1, sticky="nsew")

    def clear_entries(self):
        self.ram_string_var.set("")
        self.program_size_string_var.set("")
        self.page_size_string_var.set("")
        self.memory_model = None

    def get_current_entries(self) -> tuple[Optional[MemoryModel], Optional[str]]:
        try:
            ram = self.ram_string_var.get()

            try:
                ram = int(ram)
            except ValueError as err:
                raise ValueError("RAM ingresada no válida")

            program_size = self.program_size_string_var.get()

            try:
                program_size = int(program_size)
            except ValueError as err:
                raise ValueError("El tamaño del programa in.gresado no es válido")

            page_size = self.page_size_string_var.get()

            try:
                page_size = int(page_size)
            except ValueError as err:
                raise ValueError("El tamaño de página ingresada no es válida")

            model = MemoryModel(
                ram=ram,
                program_size=program_size,
                page_size=page_size
            )

            return model, None
        except ValidationError as err:
            return None, err.errors()[0]["msg"]
        except ValueError as err:
            return None, err.args[0]

    def enable_entries(self):
        self.ram_input.configure(state="normal")
        self.program_size_input.configure(state="normal")
        self.page_size_input.configure(state="normal")

    def disable_entries(self):
        self.ram_input.configure(state="disabled")
        self.program_size_input.configure(state="disabled")
        self.page_size_input.configure(state="disabled")

    def set_entries(self, ram: int, program_size: int, page_size: int):
        self.ram_string_var.set(str(ram))
        self.program_size_string_var.set(str(program_size))
        self.page_size_string_var.set(str(page_size))