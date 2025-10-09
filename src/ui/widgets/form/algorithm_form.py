import tkinter as tk
from tkinter import Frame

class AlgorithmForm(Frame):
    def __init__(self, master, **kwargs):
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

        self.LRU_check_button = tk.Checkbutton(self, text="LRU", variable=self.is_LRU_active)
        self.LRU_check_button.grid(row=1, column=0, sticky=tk.NSEW)
        self.FIFO_check_button = tk.Checkbutton(self, text="FIFO", variable=self.is_FIFO_active)
        self.FIFO_check_button.grid(row=1, column=1, sticky=tk.NSEW)
        self.NRU_check_button = tk.Checkbutton(self, text="NRU", variable=self.is_NRU_active)
        self.NRU_check_button.grid(row=1, column=2, sticky=tk.NSEW)
        self.CLK_check_button = tk.Checkbutton(self, text="CLK", variable=self.is_CLK_active)
        self.CLK_check_button.grid(row=2, column=0, sticky=tk.NSEW)
        self.OPTIMAL_check_button = tk.Checkbutton(self, text="OPTIMAL", variable=self.is_OPTIMAL_active)
        self.OPTIMAL_check_button.grid(row=2, column=1, sticky=tk.NSEW)