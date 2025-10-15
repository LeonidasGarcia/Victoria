import tkinter as tk
from tkinter import Frame, ttk, messagebox
from typing import Tuple, List, Optional

from pydantic import ValidationError

from src.data.preset import Preset
from src.ui.colors import victoria_background
from src.ui.widgets.form.memory_form import MemoryForm
from src.ui.widgets.form.models.memory_model import MemoryModel
from src.ui.widgets.form.models.program_model import ProgramModel
from src.ui.widgets.form.models.reference_trace_model import ReferenceTraceModel
from src.ui.widgets.form.program_form import ProgramForm


class ReferenceTraceForm(Frame):
    def __init__(self, master, memory_form: MemoryForm, program_form: ProgramForm, **kwargs):
        self.memory_form = memory_form
        self.program_form = program_form
        self.reference_trace_models: dict[str, ReferenceTraceModel] = {}

        self.selected_mode = tk.StringVar()

        super().__init__(master, **kwargs)
        self.grid_propagate(False)
        self.configure(bg=victoria_background)

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

        tk.Label(self, text="Rastreo de referencias", bg=victoria_background, fg="white").grid(row=0, column=0,
                                                                                               columnspan=2,
                                                                                               sticky=tk.W)

        tk.Label(self, text="PID", bg=victoria_background, fg="white").grid(row=1, column=0, sticky=tk.W)
        self.pid_input = tk.Entry(self, bg=victoria_background, fg="white")
        self.pid_input.grid(row=1, column=1)

        tk.Label(self, text="Número de página", bg=victoria_background, fg="white").grid(row=2, column=0, sticky=tk.W)
        self.num_page_input = tk.Entry(self, bg=victoria_background, fg="white")
        self.num_page_input.grid(row=2, column=1)

        tk.Label(self, text="Modo", bg=victoria_background, fg="white").grid(row=3, column=0, sticky=tk.W)
        self.mode_input = ttk.Combobox(self, textvariable=self.selected_mode, state="readonly")
        self.mode_input.configure(values=["r", "w"])
        self.selected_mode.set("r")
        self.mode_input.grid(row=3, column=1)

        self.register_button = tk.Button(self, text="Registrar", bg=victoria_background, fg="white",
                                         command=self.register_reference_trace)
        self.register_button.grid(row=4, column=0, columnspan=2)

        self.reference_trace_table = ttk.Treeview(self, columns=("PID", "Página", "Modo"), show="headings")
        self.reference_trace_table_setup()
        self.reference_trace_table.grid(row=1, rowspan=4, column=3, columnspan=2, sticky=tk.NSEW)

        tk.Label(self, bg=victoria_background).grid(row=0, column=2, rowspan=5, sticky=tk.NSEW, padx=5, pady=5)

        self.delete_reference_trace_button = tk.Button(self, text="Eliminar", bg=victoria_background, fg="white",
                                                       state="disabled",
                                                       command=self.on_click_delete_reference_trace_button)
        self.delete_reference_trace_button.grid(row=5, column=4)

    def reference_trace_table_setup(self):
        self.reference_trace_table.heading("PID", text="PID")
        self.reference_trace_table.heading("Página", text="Página")
        self.reference_trace_table.heading("Modo", text="Modo")

        self.reference_trace_table.column("PID", width=30)
        self.reference_trace_table.column("Página", width=60)
        self.reference_trace_table.column("Modo", width=60)

        self.reference_trace_table.bind("<<TreeviewSelect>>", self.on_reference_trace_select)

    def on_reference_trace_select(self, event):
        selected_rows = self.reference_trace_table.selection()

        if selected_rows:
            self.delete_reference_trace_button.config(state="normal")
        else:
            self.delete_reference_trace_button.config(state="disabled")

    def on_click_delete_reference_trace_button(self):
        selected_rows = self.reference_trace_table.selection()

        for row in selected_rows:
            self.reference_trace_table.delete(row)
            del self.reference_trace_models[row]

        if not self.reference_trace_table.get_children():
            self.memory_form.enable_entries()
            self.memory_form.memory_model = None
            self.program_form.enable_entries()
            self.program_form.program_model = None
            self.master.disable_entries()

    def clear_entries(self):
        self.pid_input.delete(0, tk.END)
        self.num_page_input.delete(0, tk.END)
        self.selected_mode.set("r")
        self.free_tree()

    def get_current_entries(self) -> tuple[list[ReferenceTraceModel], Optional[str]]:
        return list(self.reference_trace_models.values()), None

    def register_reference_trace(self):
        try:
            pid = self.pid_input.get()

            try:
                pid = int(pid)
            except ValueError as err:
                raise ValueError("El PID ingresado no es válido")

            page = self.num_page_input.get()

            try:
                page = int(page)
            except ValueError as err:
                raise ValueError("La página ingresada no es válida")

            mode = self.mode_input.get()

            memory_form_model, memory_form_error = self.memory_form.get_current_entries()

            if memory_form_error:
                raise ValueError(memory_form_error)

            program_form_model, program_form_error = self.program_form.get_current_entries()

            if program_form_error:
                raise ValueError(program_form_error)

            program_count = program_form_model.program_count
            page_count = memory_form_model.program_size // memory_form_model.page_size

            new_reference_trace = ReferenceTraceModel(
                program_count=program_count,
                page_count=page_count,
                pid=pid,
                page=page,
                mode=mode
            )

            pid = new_reference_trace.pid
            page = new_reference_trace.page
            mode = new_reference_trace.mode

            new_id = self.reference_trace_table.insert("", "end", values=(pid, page, mode))
            self.reference_trace_models[new_id] = new_reference_trace

            if len(self.reference_trace_table.get_children()) == 1:
                self.memory_form.disable_entries()
                self.memory_form.memory_model = memory_form_model
                self.program_form.disable_entries()
                self.program_form.program_model = program_form_model
                self.master.check_if_can_start()

        except ValidationError as err:
            messagebox.showerror("Error en el formulario", err.errors()[0]["msg"])
        except ValueError as err:
            messagebox.showerror("Error en el formulario", err.args[0])

    def free_tree(self):
        tree_children = self.reference_trace_table.get_children()
        self.reference_trace_table.delete(*tree_children)
        self.reference_trace_models = {}

    def set_entries(self, memory_form_model: MemoryModel, program_form_model: ProgramModel,
                    reference_trace: list[tuple[int, int, int, str]]):
        self.free_tree()

        program_count = program_form_model.program_count
        page_count = memory_form_model.program_size // memory_form_model.page_size

        for _, pid, page, mode in reference_trace:
            new_reference_trace = ReferenceTraceModel(
                program_count=program_count,
                page_count=page_count,
                pid=int(pid),
                page=int(page),
                mode=mode
            )

            new_id = self.reference_trace_table.insert("", "end", values=(pid, page, mode))
            self.reference_trace_models[new_id] = new_reference_trace

        if len(self.reference_trace_table.get_children()) != 0:
            self.memory_form.disable_entries()
            self.memory_form.memory_model = memory_form_model
            self.program_form.disable_entries()
            self.program_form.program_model = program_form_model
            self.master.check_if_can_start()
