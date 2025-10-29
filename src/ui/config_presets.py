import tkinter as tk
from tkinter import Toplevel, ttk, messagebox

from src.data.preset import Preset
from src.data.presets_central import presets_central
from src.ui.colors import victoria_background
from src.ui.widgets.form.memory_form import MemoryForm
from src.ui.widgets.form.program_form import ProgramForm
from src.ui.widgets.form.reference_trace_form import ReferenceTraceForm


class ConfigPresets(Toplevel):
    def __init__(self, master, **kwargs):
        self.selected_preset_input = tk.StringVar()
        self.selected_preset: Preset | None = None

        super().__init__(master, **kwargs)
        self.configure(bg=victoria_background, padx=20, pady=20)
        self.title("Configuración de Presets")
        self.geometry("550x890")
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(4, weight=5)
        self.grid_rowconfigure(6, weight=20)

        self.controls_frame = tk.Frame(self, bg=victoria_background)

        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, weight=1)
        self.controls_frame.grid_columnconfigure(3, weight=1)
        self.controls_frame.grid_rowconfigure(0, weight=1)

        self.controls_frame.grid(row=0, column=0, sticky="nsew")

        self.presets_combobox = ttk.Combobox(self.controls_frame, textvariable=self.selected_preset_input,
                                             state="readonly")
        self.presets_combobox.grid(row=0, column=0, sticky="nsew")

        self.save_button = tk.Button(self.controls_frame, text="Guardar", bg=victoria_background, fg="white",
                                     command=self.update_preset)
        self.save_button.grid(row=0, column=1, sticky="nsew")

        self.reset_button = tk.Button(self.controls_frame, text="Reiniciar", bg=victoria_background, fg="white",
                                      command=lambda: self.set_fields())
        self.reset_button.grid(row=0, column=2, sticky="nsew")

        self.delete_button = tk.Button(self.controls_frame, text="Borrar", bg=victoria_background, fg="white",
                                       command=self.delete_preset)
        self.delete_button.grid(row=0, column=3, sticky="nsew")

        tk.Frame(self, bg=victoria_background).grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.memory_form = MemoryForm(self, bg=victoria_background)
        self.memory_form.grid(row=2, column=0, sticky=tk.NSEW)

        tk.Frame(self, bg=victoria_background).grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.program_form = ProgramForm(self)
        self.program_form.grid(row=4, column=0, sticky=tk.NSEW)

        tk.Frame(self, bg=victoria_background).grid(row=5, column=0, sticky="nsew", padx=10, pady=10)

        bottom_frame = tk.Frame(self, bg=victoria_background)

        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

        bottom_frame.grid(row=6, column=0, sticky="nsew")

        self.reference_trace_form = ReferenceTraceForm(bottom_frame, memory_form=self.memory_form,
                                                       program_form=self.program_form)
        self.reference_trace_form.grid(row=0, column=0, sticky=tk.NSEW)

        self.reload_presets()
        self.set_fields()

        self.presets_combobox.bind("<<ComboboxSelected>>", lambda event: self.on_selection_change())

    def delete_preset(self):
        presets_central.delete_preset(preset_id=self.selected_preset.id)
        messagebox.showinfo("Eliminar preset", "Preset eliminado con éxito")
        self.reload_presets()
        self.set_fields()

    def reload_presets(self):
        loaded_presets = presets_central.get_presets()
        presets = [preset.name for preset in loaded_presets]
        self.presets_combobox.configure(values=presets)
        # trickyyy!!!
        self.selected_preset_input.set(presets[0])
        self.selected_preset = loaded_presets[0]

    def on_selection_change(self):
        self.selected_preset = presets_central.get_preset(preset_name=self.selected_preset_input.get())
        self.set_fields()

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

    def update_preset(self):
        selected_preset = self.selected_preset
        memory_form_model, error = self.memory_form.get_current_entries()

        if error:
            raise RuntimeError(error)

        program_form_model, error = self.program_form.get_current_entries()

        if error:
            raise RuntimeError(error)

        reference_trace_models, error = self.reference_trace_form.get_current_entries()

        if error:
            raise RuntimeError(error)

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

        presets_central.delete_preset(selected_preset.id)
        selected_preset.id = -1
        self.selected_preset, _ = presets_central.save_preset(selected_preset)
        self.set_fields()

    def check_if_can_start(self):
        if self.reference_trace_form.reference_trace_table.get_children():
            self.enable_entries()

    def disable_entries(self):
        self.save_button.configure(state="disabled")

    def enable_entries(self):
        self.save_button.config(state="normal")
