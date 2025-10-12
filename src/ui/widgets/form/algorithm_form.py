import tkinter as tk
from tkinter import Frame
from typing import Optional

from pydantic import ValidationError

from src.ui.widgets.form.models.algoritm_model import AlgorithmModel


class AlgorithmForm(Frame):
    def __init__(self, master, **kwargs):
        self.algorithm_model: Optional[AlgorithmModel] = None
        self.valid_state = False

        self.is_LRU_active = tk.BooleanVar()
        self.is_FIFO_active = tk.BooleanVar()
        self.is_NRU_active = tk.BooleanVar()
        self.is_CLK_active = tk.BooleanVar()
        self.is_OPTIMAL_active = tk.BooleanVar()

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        tk.Label(self, text="Algoritmos de reemplazo").grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.LRU_check_button = tk.Checkbutton(self, text="LRU", variable=self.is_LRU_active, command=self.check_at_least_one)
        self.LRU_check_button.grid(row=1, column=0, sticky=tk.NSEW)
        self.FIFO_check_button = tk.Checkbutton(self, text="FIFO", variable=self.is_FIFO_active, command=self.check_at_least_one)
        self.FIFO_check_button.grid(row=1, column=1, sticky=tk.NSEW)
        self.NRU_check_button = tk.Checkbutton(self, text="NRU", variable=self.is_NRU_active, command=self.check_at_least_one)
        self.NRU_check_button.grid(row=1, column=2, sticky=tk.NSEW)
        self.CLK_check_button = tk.Checkbutton(self, text="CLK", variable=self.is_CLK_active, command=self.check_at_least_one)
        self.CLK_check_button.grid(row=2, column=0, sticky=tk.NSEW)
        self.OPTIMAL_check_button = tk.Checkbutton(self, text="OPTIMAL", variable=self.is_OPTIMAL_active, command=self.check_at_least_one)
        self.OPTIMAL_check_button.grid(row=2, column=1, sticky=tk.NSEW)

    def clear_entries(self):
        self.is_LRU_active.set(False)
        self.is_FIFO_active.set(False)
        self.is_NRU_active.set(False)
        self.is_CLK_active.set(False)
        self.is_OPTIMAL_active.set(False)
        self.algorithm_model = None

    def get_current_entries(self) -> tuple[Optional[AlgorithmModel], Optional[str]]:
        try:
            is_LRU_active = self.is_LRU_active.get()
            is_FIFO_active = self.is_FIFO_active.get()
            is_NRU_active = self.is_NRU_active.get()
            is_CLK_active = self.is_CLK_active.get()
            is_OPTIMAL_active = self.is_OPTIMAL_active.get()

            model = AlgorithmModel(
                lru=is_LRU_active,
                fifo=is_FIFO_active,
                nru=is_NRU_active,
                clk=is_CLK_active,
                optimal=is_OPTIMAL_active,
            )

            return model, None
        except ValidationError as err:
            return None, err.errors()[0]["msg"]
        except ValueError as err:
            return None, err.args[0]

    def check_at_least_one(self):
        is_LRU_active = self.is_LRU_active.get()
        is_FIFO_active = self.is_FIFO_active.get()
        is_NRU_active = self.is_NRU_active.get()
        is_CLK_active = self.is_CLK_active.get()
        is_OPTIMAL_active = self.is_OPTIMAL_active.get()

        if (is_LRU_active or is_FIFO_active or is_NRU_active or is_CLK_active or is_OPTIMAL_active):
            self.valid_state = True
            self.master.check_if_can_start()
        else:
            self.master.disable_entries()
            self.valid_state = False
