import tkinter as tk

from src.ui.widgets.core.top_bar.top_bar import TopBar

victoria_ui = tk.Tk()
victoria_ui.title("Victoria")
victoria_ui.geometry("1600x800")

victoria_ui.grid_columnconfigure(0, weight=1)
victoria_ui.grid_rowconfigure(2, weight=1)

top_bar= TopBar(victoria_ui, height="80px")