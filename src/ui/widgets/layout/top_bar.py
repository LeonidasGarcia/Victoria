import tkinter as tk
from tkinter import Frame
from tkinter.font import Font

from src.ui.colors import victoria_background, victoria_orange, victoria_lightblue
from src.ui.config_presets import ConfigPresets
from src.ui.widgets.extra.victoria_label import VictoriaLabel
from src.ui.widgets.layout.body import Body
from src.util.svg_conversor import load_svg_icon


class TopBar(Frame):

    def __init__(self, master, body: Body, **kwargs):
        self.svg_icon = None
        self.body = body

        self.title = None
        self.welcome_page_button = None
        self.simulate_page_button = None
        self.config_page_button = None

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self, bg=victoria_background)
        self.main_frame_setup()

        self.config_frame = tk.Frame(self, bg=victoria_background)
        self.config_frame_setup()

    def main_frame_setup(self):
        main_frame = self.main_frame
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_propagate(False)

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1, minsize=200)
        main_frame.columnconfigure(2, weight=1, minsize=200)
        main_frame.rowconfigure(0, weight=1)

        title = VictoriaLabel(main_frame, bg=victoria_background, width=500)
        title.grid(row=0, column=0, sticky="nsew")

        welcome_page_button = tk.Button(main_frame, text="Inicio", bg=victoria_background, fg=victoria_orange,
                                        font=Font(family="Sans Serif", size=14, weight="bold"),
                                        cursor="hand2",
                                        command=lambda: self.body.load_start_screen())
        welcome_page_button.grid(row=0, column=1, sticky="nsew")

        simulate_page_button = tk.Button(main_frame, text="Simular", bg=victoria_background, fg=victoria_lightblue,
                                         cursor="hand2",
                                         font=Font(family="Sans Serif", size=14, weight="bold"),
                                         command=lambda: self.body.load_form_screen())
        simulate_page_button.grid(row=0, column=2, sticky="nsew")

        self.title = title
        self.welcome_page_button = welcome_page_button
        self.simulate_page_button = simulate_page_button

    def config_frame_setup(self):
        config_frame = self.config_frame
        config_frame.grid(row=0, column=1, sticky="nsew")
        config_frame.grid_propagate(False)

        config_frame.columnconfigure(0, weight=1)
        config_frame.rowconfigure(0, weight=1)

        spacer = tk.Frame(config_frame, bg=victoria_background)
        spacer.grid(row=0, column=0, sticky="nsew")

        self.svg_icon = load_svg_icon("../assets/config_icon.svg", (46, 46))

        config_page_button = tk.Button(config_frame, width=100, image=self.svg_icon, bg=victoria_background,
                                       cursor="hand2",
                                       command=lambda: ConfigPresets(self.winfo_toplevel()))
        config_page_button.grid(row=0, column=1, sticky="ns")

        self.config_page_button = config_page_button
