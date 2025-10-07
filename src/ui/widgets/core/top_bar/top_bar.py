import tkinter as tk
from tkinter import Frame

from src.ui.colors import victoria_background, primary_text_color
from src.ui.widgets.core.top_bar.victoria_label import VictoriaLabel
from src.util.svg_conversor import load_svg_icon


class TopBar(Frame):

    def __init__(self, master, **kwargs):
        self.svg_icon = None

        super().__init__(master, bg=victoria_background, **kwargs)
        self.grid_propagate(False)
        self.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self, bg="red")
        self.main_frame_setup()

        self.config_frame = tk.Frame(self, bg=victoria_background)
        self.config_frame_setup()

    def main_frame_setup(self):
        main_frame = self.main_frame
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_propagate(False)

        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)

        title = VictoriaLabel(main_frame, bg=victoria_background)
        title.grid(row=0, column=0, sticky="nsew")

        welcome_page_button = tk.Button(main_frame, text="Inicio", bg=victoria_background,)
        welcome_page_button.grid(row=0, column=1, sticky="nsew")

        simulate_page_button = tk.Button(main_frame, text="Simular", bg=victoria_background)
        simulate_page_button.grid(row=0, column=2, sticky="nsew")

    def config_frame_setup(self):
        config_frame = self.config_frame
        config_frame.grid(row=0, column=1, sticky="nsew")
        config_frame.grid_propagate(False)

        config_frame.columnconfigure(0, weight=1)
        config_frame.rowconfigure(0, weight=1)

        spacer = tk.Frame(config_frame, bg=victoria_background)
        spacer.grid(row=0, column=0, sticky="nsew")

        self.svg_icon = load_svg_icon("../assets/config_icon.svg", (46, 46))

        config_button = tk.Button(config_frame, width=100, image=self.svg_icon, bg=victoria_background)
        config_button.grid(row=0, column=1, sticky="ns")