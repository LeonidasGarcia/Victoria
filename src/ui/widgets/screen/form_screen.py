import random
import tkinter as tk
from tkinter import Frame, ttk, simpledialog, messagebox
from typing import Optional, List

from src.core.algorithms.clk import Clk
from src.core.algorithms.fifo import Fifo
from src.core.algorithms.lru import Lru
from src.core.algorithms.nru import Nru
from src.core.algorithms.optimal import Optimal
from src.core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm
from src.core.victoria import Victoria
from src.data.preset import Preset
from src.data.presets_central import presets_central
from src.ui.colors import victoria_background
from src.ui.widgets.form.algorithm_form import AlgorithmForm
from src.ui.widgets.form.memory_form import MemoryForm
from src.ui.widgets.form.program_form import ProgramForm
from src.ui.widgets.form.reference_trace_form import ReferenceTraceForm
from src.util.metrics import Metrics


class FormScreen(Frame):
    def __init__(self, master, **kwargs):
        self.selected_preset_input = tk.StringVar()
        self.selected_preset: Preset | None = None

        super().__init__(master, **kwargs)
        self.grid_propagate(False)
        self.configure(bg=victoria_background, padx=30, pady=30)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)

        self.presets_combobox = ttk.Combobox(self, textvariable=self.selected_preset_input, state="readonly")
        self.presets_combobox.grid(row=0, column=0, sticky="w")

        self.memory_form = MemoryForm(self, bg=victoria_background)
        self.memory_form.grid(row=1, column=0, rowspan=2, sticky=tk.NSEW)

        self.algorithm_form = AlgorithmForm(self)
        self.algorithm_form.grid(row=3, column=0, sticky=tk.NSEW)

        tk.Frame(self, bg=victoria_background).grid(row=0, column=1, rowspan=4, sticky=tk.NSEW, padx=20, pady=20)

        self.program_form = ProgramForm(self)
        self.program_form.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW)

        self.reference_trace_form = ReferenceTraceForm(self, memory_form=self.memory_form,
                                                       program_form=self.program_form)
        self.reference_trace_form.grid(row=2, rowspan=2, column=2, sticky=tk.NSEW)

        tk.Frame(self, bg=victoria_background).grid(row=0, column=3, rowspan=4, sticky=tk.NSEW, padx=20, pady=20)

        self.start_frame = tk.Frame(self, bg=victoria_background)

        self.start_frame.grid_columnconfigure(0, weight=1)
        self.start_frame.grid_rowconfigure(0, weight=1)
        self.start_frame.grid_rowconfigure(1, weight=1)
        self.start_frame.grid_rowconfigure(2, weight=1)

        self.start_frame.grid(row=0, rowspan=4, column=4, sticky=tk.NSEW)

        self.save_button = tk.Button(self.start_frame, bg=victoria_background, fg="white", text="Guardar como preset",
                                     state="normal",
                                     command=self.save_preset)
        self.save_button.grid(row=0, column=0, sticky="s")

        self.start_button = tk.Button(self.start_frame, bg=victoria_background, fg="white", text="Iniciar",
                                      state=tk.DISABLED, command=self.load_simulation)
        self.start_button.grid(row=1, column=0)

        self.random_button = tk.Button(self.start_frame, bg=victoria_background, fg="white", text="Accesos aleatorios",
                                       command=self.load_random)
        self.random_button.grid(row=2, column=0, sticky="n")

        self.reload_presets()

        self.presets_combobox.bind("<<ComboboxSelected>>", lambda event: self.on_selection_change())

    def load_random(self):
        random_page_size = random.randint(2, 10)
        random_program_size = random_page_size * random.randint(2, 90)
        random_ram = random_page_size * random.randint(2, 10)

        random_program_count = random.randint(1, 50)

        victoria_sample = Victoria(ram=random_ram, program_size=random_program_size, page_size=random_page_size,
                                   pra=Lru(), metrics=Metrics())

        for i in range(random_program_count):
            victoria_sample.load_program(pid=i, name=f"Program {i + 1}", data=str(i))

        request_count = random.randint(1, 100)
        victoria_sample.generate_random_requests(quantity=request_count)

        random_reference_trace: list[tuple[int, int, int, str]] = []
        for pid, page, mode in victoria_sample.requests:
            random_reference_trace.append((-1, pid, page, mode))

        self.memory_form.set_entries(
            ram=random_ram,
            program_size=random_program_size,
            page_size=random_page_size,
        )

        self.program_form.set_entries(
            program_count=random_program_count
        )

        memory_form_model, error = self.memory_form.get_current_entries()

        if error:
            raise ValueError(error)

        program_form_model, error = self.program_form.get_current_entries()

        if error:
            raise ValueError(error)

        self.reference_trace_form.set_entries(
            memory_form_model=memory_form_model,
            program_form_model=program_form_model,
            reference_trace=random_reference_trace,
        )

    def save_preset(self):
        if self.selected_preset_input.get() != "Personalizado":
            return

        selected_preset = Preset()
        memory_form_model, error = self.memory_form.get_current_entries()

        if error:
            messagebox.showerror("Error", error)
            return

        program_form_model, error = self.program_form.get_current_entries()

        if error:
            messagebox.showerror("Error", error)
            return

        reference_trace_models, error = self.reference_trace_form.get_current_entries()

        if error:
            messagebox.showerror("Error", error)
            return

        selected_preset.ram = memory_form_model.ram
        selected_preset.program_size = memory_form_model.program_size
        selected_preset.page_size = memory_form_model.page_size

        selected_preset.program_count = program_form_model.program_count

        new_reference_trace = []
        for reference_trace_model in reference_trace_models:
            new_reference_trace.append(
                (
                    -1,
                    reference_trace_model.pid,
                    reference_trace_model.page,
                    reference_trace_model.mode
                )
            )

        selected_preset.reference_trace = new_reference_trace

        selected_preset.name = simpledialog.askstring("Nombre del nuevo preset", "Introduce el nombre de este preset",
                                                      parent=self.winfo_toplevel())

        self.selected_preset, error = presets_central.save_preset(selected_preset)

        if error:
            messagebox.showerror("Error", error)
        else:
            self.reload_presets()
            self.clear_entries()

    def on_selection_change(self):
        self.selected_preset = presets_central.get_preset(preset_name=self.selected_preset_input.get())
        if self.selected_preset:
            self.set_fields()
            self.save_button.config(state="disabled")
        else:
            self.clear_entries()
            self.save_button.config(state="normal")

    def clear_entries(self):
        self.memory_form.clear_entries()
        self.memory_form.enable_entries()
        self.algorithm_form.clear_entries()
        self.program_form.clear_entries()
        self.program_form.enable_entries()
        self.reference_trace_form.clear_entries()
        self.selected_preset = None

    def reload_presets(self):
        loaded_presets = presets_central.get_presets()
        presets = ["Personalizado"] + [preset.name for preset in loaded_presets]

        self.presets_combobox.configure(values=presets)
        # trickyyy!!!
        self.selected_preset_input.set(presets[0])
        if self.selected_preset_input.get() != "Personalizado":
            self.selected_preset = loaded_presets[0]
        else:
            self.selected_preset = None

    def set_fields(self):
        current_preset = self.selected_preset

        if not current_preset:
            raise RuntimeError("Error interno, esto no debería pasar")

        self.memory_form.set_entries(
            ram=current_preset.ram,
            program_size=current_preset.program_size,
            page_size=current_preset.page_size
        )

        self.program_form.set_entries(
            program_count=current_preset.program_count
        )

        memory_form_model, error = self.memory_form.get_current_entries()

        if error:
            raise ValueError(error)

        program_form_model, error = self.program_form.get_current_entries()

        if error:
            raise ValueError(error)

        self.reference_trace_form.set_entries(
            memory_form_model=memory_form_model,
            program_form_model=program_form_model,
            reference_trace=current_preset.reference_trace
        )

    def check_if_can_start(self):
        if self.algorithm_form.valid_state and self.reference_trace_form.reference_trace_table.get_children():
            self.enable_entries()

    def enable_entries(self):
        self.save_button.configure(state="normal")
        self.start_button.configure(state="normal")

    def disable_entries(self):
        self.save_button.configure(state="disabled")
        self.start_button.configure(state="disabled")

    def load_simulation(self):
        memory_form_model = self.memory_form.memory_model
        program_form_model = self.program_form.program_model
        algorithm_form_model = self.algorithm_form.get_current_entries()[0]
        reference_trace = list(self.reference_trace_form.reference_trace_models.values())

        ram = memory_form_model.ram
        program_size = memory_form_model.program_size
        page_size = memory_form_model.page_size

        algoritms_to_load: List[tuple[bool, type[PageReplacementAlgorithm]]] = [
            (algorithm_form_model.lru, Lru),
            (algorithm_form_model.fifo, Fifo),
            (algorithm_form_model.nru, Nru),
            (algorithm_form_model.clk, Clk),
            (algorithm_form_model.optimal, Optimal)
        ]

        victoria_units: List[Victoria] = []

        for selected, Pra in algoritms_to_load:
            if selected:
                victoria = Victoria(ram=ram, program_size=program_size, page_size=page_size, pra=Pra(),
                                    metrics=Metrics())
                victoria_units.append(victoria)

        self.master.create_simulate_screen(victoria_units=victoria_units,
                                           program_count=program_form_model.program_count,
                                           reference_trace=reference_trace)
