from tkinter import Frame

from src.core.algorithms.clk import Clk
from src.core.victoria import Victoria
from src.ui.widgets.screen.form_screen import FormScreen
from src.ui.widgets.screen.simulate_screen import SimulateScreen
from src.ui.widgets.screen.start_screen import StartScreen
from src.util.metrics import Metrics


class Body(Frame):
    def __init__(self, master, **kwargs):
        self.current_child = list()

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        simulate_screen = SimulateScreen(self, victoria_units=[Victoria(pra=Clk(), metrics=Metrics(), ram=204800, program_size=24576, page_size=4096), Victoria(pra=Clk(), metrics=Metrics(), ram=204800, program_size=24576, page_size=4096), Victoria(pra=Clk(), metrics=Metrics(), ram=204800, program_size=24576, page_size=4096)])
        simulate_screen.grid(row=0, column=0, sticky="nsew")