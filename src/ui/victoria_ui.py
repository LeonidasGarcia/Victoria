import tkinter as tk

from src.ui.colors import victoria_background
from src.ui.config_presets import ConfigPresets
from src.ui.widgets.layout.navigator import Navigator
from src.ui.widgets.layout.top_bar import TopBar
from src.ui.widgets.layout.body import Body

victoria_ui = tk.Tk()
victoria_ui.title("Victoria")
victoria_ui.geometry("1600x800")
victoria_ui.configure(bg=victoria_background)
victoria_ui.resizable(width=False, height=False)

victoria_ui.grid_columnconfigure(0, weight=1)
victoria_ui.grid_rowconfigure(0, weight=1)

main_frame = tk.Frame(victoria_ui, bg=victoria_background)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

body = Body(main_frame, bg=victoria_background)
body.grid(row=1, column=0, sticky="nsew")

top_bar = TopBar(main_frame, height="80px", body=body, bg=victoria_background)
top_bar.grid(row=0, column=0, sticky="nsew")
