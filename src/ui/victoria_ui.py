import tkinter as tk

from src.ui.colors import victoria_background
from src.ui.config_presets import ConfigPresets
from src.ui.widgets.layout.navigator import Navigator
from src.ui.widgets.layout.top_bar import TopBar
from src.ui.widgets.layout.body import Body

victoria_ui = tk.Tk()
victoria_ui.title("Victoria")
victoria_ui.geometry("1600x800")

victoria_ui.grid_columnconfigure(0, weight=1)
victoria_ui.grid_rowconfigure(2, weight=1)

navigator = Navigator(victoria_ui, height="30px", bg=victoria_background)
navigator.grid(row=1, column=0, sticky="nsew")

body = Body(victoria_ui, bg=victoria_background)
body.grid(row=2, column=0, sticky="nsew")

top_bar= TopBar(victoria_ui, height="80px", body=body, bg=victoria_background)
top_bar.grid(row=0, column=0, sticky="nsew")

