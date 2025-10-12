import tkinter as tk
from tkinter import Frame
from typing import Optional

from pydantic import ValidationError

from src.ui.widgets.form.models.program_model import ProgramModel


class ProgramForm(Frame):
    def __init__(self, master, **kwargs):
        self.program_model: Optional[ProgramModel] = None

        self.program_count_string_var = tk.StringVar()

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        tk.Label(self, text="Programas").grid(row=0, column=0, sticky=tk.W)

        tk.Label(self, text="Número de programas").grid(row=1, column=0, sticky=tk.W)
        self.program_count_input = tk.Entry(self, textvariable=self.program_count_string_var)
        self.program_count_input.grid(row=1, column=1, sticky=tk.NSEW)

    def clear_entries(self):
        self.program_count_string_var.set("")
        self.program_model = None

    def get_current_entries(self) -> tuple[Optional[ProgramModel], Optional[str]]:
        try:
            program_count = self.program_count_string_var.get()

            try:
                program_count = int(program_count)
            except ValueError as err:
                raise ValueError("La cantidad de programas ingresada no es válida")

            model = ProgramModel(
                program_count=program_count,
            )

            return model, None
        except ValidationError as err:
            return None, err.errors()[0]["msg"]
        except ValueError as err:
            return None, err.args[0]

    def enable_entries(self):
        self.program_count_input.configure(state="normal")

    def disable_entries(self):
        self.program_count_input.configure(state="disabled")

    def set_entries(self, program_count: int) -> None:
        self.program_count_string_var.set(str(program_count))