from tkinter import Frame
from typing import List, Optional

from src.core.victoria import Victoria
from src.ui.widgets.form.models.reference_trace_model import ReferenceTraceModel
from src.ui.widgets.screen.form_screen import FormScreen
from src.ui.widgets.screen.simulate_screen import SimulateScreen
from src.ui.widgets.screen.start_screen import StartScreen


class Body(Frame):
    def __init__(self, master, **kwargs):
        self.current_child = list()

        super().__init__(master, **kwargs)
        self.grid_propagate(False)
        self.configure(padx=15, pady=15)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.start_screen = StartScreen(self)
        self.form_screen = FormScreen(self)
        self.simulate_screen: Optional[SimulateScreen] = None

        self.current_screen = self.start_screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")

        self.load_start_screen()

    def load_start_screen(self):
        self.winfo_toplevel().title("Victoria")
        self.current_screen.grid_remove()

        if self.simulate_screen:
            self.simulate_screen.stop_simulation()
            self.simulate_screen.destroy()

        self.current_screen = self.start_screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")

    def load_form_screen(self):
        self.winfo_toplevel().title("Datos para la simulación")
        self.current_screen.grid_remove()

        if self.simulate_screen:
            self.simulate_screen.stop_simulation()
            self.simulate_screen.destroy()

        self.current_screen = self.form_screen
        self.form_screen.grid(row=0, column=0, sticky="nsew")

    def create_simulate_screen(self, victoria_units: List[Victoria], program_count: int,
                               reference_trace: List[ReferenceTraceModel]):
        self.winfo_toplevel().title("Ejecución en progreso...")
        self.current_screen.grid_remove()

        if self.simulate_screen:
            self.simulate_screen.stop_simulation()
            self.simulate_screen.destroy()

        self.simulate_screen = SimulateScreen(self, victoria_units, program_count=program_count,
                                              reference_trace=reference_trace)
        self.current_screen = self.simulate_screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")
