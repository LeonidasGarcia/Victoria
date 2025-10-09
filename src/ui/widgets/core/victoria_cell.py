import tkinter as tk
from tkinter import Frame, Label, Button, ttk
from typing import Optional, List

from src.core.victoria import Victoria
from src.ui.colors import victoria_background
from src.util.lib import calculate_rows_and_columns


def saludo():
    print("saludo")

class VictoriaCell(Frame):
    _BREAKPOINT = 350

    def __init__(self, master, victoria: Victoria, **kwargs):
        self.victoria: Victoria = victoria
        self.victoria.load_program(0, "hola", "blue")
        self.victoria.load_program(1, "hola", "red")
        self.victoria.load_program(2, "hola", "green")
        self.victoria.load_program(3, "hola", "blue")
        self.victoria.load_program(4, "hola", "red")
        self.victoria.load_program(5, "hola", "green")
        self.victoria.load_program(6, "hola", "blue")
        self.victoria.load_program(7, "hola", "red")
        self.victoria.load_program(8, "hola", "green")
        self.victoria.load_program(9, "hola", "green")
        self.victoria.load_program(10, "hola", "green")

        self.victoria.load_program(11, "hola", "green")

        self.victoria.generate_random_requests(100)

        self.current_request_label: Optional[Label] = None
        self.change_frame_view_button: Optional[Button] = None
        self.cell_frame: Optional[Frame] = None
        self.cells: List[Label] = []

        self.metrics_frame: Optional[Frame] = None
        self.logic_time_label: Optional[Label] = None
        self.page_fault_count_label: Optional[Label] = None
        self.page_fault_rate_label: Optional[Label] = None
        self.average_time_accesses_label: Optional[Label] = None
        self.memory_usage_label: Optional[Label] = None

        self.programs_frame: Optional[Frame] = None

        self.is_wide_layout: bool = False

        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=6)

        self.top_frame = tk.Frame(self, bg="red")
        self.top_frame_setup()
        self.top_frame.grid(row=0, column=0, sticky="nsew")

        self.mid_frame = tk.Frame(self, bg=victoria_background)
        self.mid_frame_setup()
        self.mid_frame.grid(row=1, column=0, sticky="nsew")

        self.bottom_frame = tk.Frame(self, bg=victoria_background)
        self.bottom_frame_setup()
        self.bottom_frame.grid(row=2, column=0, sticky="nsew")

        self.bind("<Configure>", self._check_size)
        self.execute_current_request()

    def execute_current_request(self):
        current_request_data = self.victoria.get_current_request_data()
        self.victoria.execute_next_request()

        current_request = current_request_data["current_request"]
        metrics = current_request_data["metrics"]

        self.current_request_label.configure(text=f"{current_request[0]} accediendo a la pagina {current_request[1]} en modo {current_request[2]}")

        self.logic_time_label.configure(text=metrics["logic_time"])
        self.page_fault_count_label.configure(text=metrics["page_fault_count"])
        self.page_fault_rate_label.configure(text=metrics["page_fault_rate"])
        self.average_time_accesses_label.configure(text=metrics["average_time_access"])
        self.memory_usage_label.configure(text=metrics["memory_usage"])

        page_frames = self.victoria.ram_manager.ram

        for i, color in enumerate(page_frames):
            current_cell = self.cells[i]
            if color == "":
                color = victoria_background
            current_cell.configure(bg=color)

        self.after(1000, self.execute_current_request)

    def top_frame_setup(self):
        top_frame = self.top_frame

        top_frame.grid_columnconfigure(0, weight=5)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_rowconfigure(0, weight=1)

        current_request = tk.Label(top_frame, text="hola", bg="yellow")
        current_request.grid(row=0, column=0, sticky="nsew")

        change_frame_view_button = tk.Button(top_frame, text="change view", bg="red")
        change_frame_view_button.grid(row=0, column=1, sticky="nsew")

        self.current_request_label = current_request
        self.change_frame_view_button = change_frame_view_button

    def mid_frame_setup(self):
        mid_frame = self.mid_frame

        mid_frame.grid_columnconfigure(0, weight=1)
        mid_frame.grid_rowconfigure(0, weight=1)

        cell_frame = tk.Frame(mid_frame, bg=victoria_background)

        page_frames = self.victoria.ram_manager.ram
        columns, rows = calculate_rows_and_columns(len(page_frames))

        current_page_frame = 0
        stop_flag = False
        for i in range(rows):
            for j in range(columns):
                cell_frame.grid_columnconfigure(j, weight=1)
                cell = tk.Label(cell_frame, text=current_page_frame, borderwidth=1, relief="ridge")
                cell.grid(row=i, column=j, sticky="nsew")
                self.cells.append(cell)
                current_page_frame += 1
                if current_page_frame == len(page_frames):
                    stop_flag = True
                    break
            cell_frame.grid_rowconfigure(i, weight=1)
            if stop_flag:
                break

        cell_frame.grid(row=0, column=0, sticky="nsew")
        self.cell_frame = cell_frame

    def bottom_frame_setup(self):
        bottom_frame = self.bottom_frame

        bottom_frame.grid_columnconfigure(0, weight=0)
        bottom_frame.grid_columnconfigure(1, weight=0)
        bottom_frame.grid_rowconfigure(0, weight=1)

        metrics_frame = tk.Frame(bottom_frame, bg="cyan")

        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_rowconfigure(0, weight=1)
        metrics_frame.grid_rowconfigure(1, weight=1)
        metrics_frame.grid_rowconfigure(2, weight=1)
        metrics_frame.grid_rowconfigure(3, weight=1)
        metrics_frame.grid_rowconfigure(4, weight=1)

        metrics_frame.grid(row=0, column=0, sticky="nsew")

        current_request_data =self.victoria.get_current_request_data()["metrics"]

        self.logic_time_label = tk.Label(metrics_frame, text=current_request_data["logic_time"])
        self.logic_time_label.grid(row=0, column=0, sticky="nsew")

        self.page_fault_count_label = tk.Label(metrics_frame, text=current_request_data["page_fault_count"])
        self.page_fault_count_label.grid(row=1, column=0, sticky="nsew")

        self.page_fault_rate_label = tk.Label(metrics_frame, text=current_request_data["page_fault_rate"])
        self.page_fault_rate_label.grid(row=2, column=0, sticky="nsew")

        self.average_time_accesses_label = tk.Label(metrics_frame, text=current_request_data["average_time_access"])
        self.average_time_accesses_label.grid(row=3, column=0, sticky="nsew")

        self.memory_usage_label = tk.Label(metrics_frame, text=current_request_data["memory_usage"])
        self.memory_usage_label.grid(row=4, column=0, sticky="nsew")

        programs_frame = tk.Frame(bottom_frame, bg="blue")

        programs_frame.columnconfigure(0, weight=1)
        programs_frame.columnconfigure(1, weight=0)
        programs_frame.rowconfigure(0, weight=1)

        programs_frame.grid(row=0, column=1, sticky="nsew")

        canvas = tk.Canvas(programs_frame, borderwidth=0, bg=victoria_background)

        canvas.grid_columnconfigure(0, weight=1)
        canvas.grid_rowconfigure(0, weight=1)

        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(programs_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        wrapper_program_frame = tk.Frame(canvas)

        wrapper_program_frame.grid_columnconfigure(0, weight=1)

        id_child = canvas.create_window((0, 0), window=wrapper_program_frame, anchor="nw")

        wrapper_program_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(id_child, width=event.width))

        programs = self.victoria.programs

        for i, program in programs.items():
            program_frame = tk.Frame(wrapper_program_frame, bg=victoria_background)

            program_frame.grid_columnconfigure(0, weight=0)
            program_frame.grid_columnconfigure(1, weight=1)
            program_frame.grid_rowconfigure(0, weight=1)

            program_frame.grid(row=i, column=0, sticky="nsew")
            tk.Label(program_frame, bg=program.data, width=5, height=2).grid(row=0, column=0)
            tk.Label(program_frame, text=program.name).grid(row=0, column=1, sticky="nsew")

        self.metrics_frame = metrics_frame
        self.programs_frame = programs_frame

    def _check_size(self, event):
        current_width = self.winfo_width()

        if current_width == 0 and event is None:
            return

        if current_width >= self._BREAKPOINT:
            if not self.is_wide_layout:
                self._apply_wide_layout()
                self.is_wide_layout = True
        else:
            if self.is_wide_layout:
                self._apply_compact_layout()
                self.is_wide_layout = False

    def _apply_wide_layout(self):
        bottom_frame = self.bottom_frame

        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(1, weight=0)

        metrics_frame = self.metrics_frame
        programs_frame = self.programs_frame

        metrics_frame.grid_remove()
        programs_frame.grid_remove()

        metrics_frame.grid(row=0, column=0, sticky="nsew")
        programs_frame.grid(row=0, column=1, sticky="nsew")

    def _apply_compact_layout(self):
        bottom_frame = self.bottom_frame

        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=0)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(1, weight=1)

        metrics_frame = self.metrics_frame
        programs_frame = self.programs_frame

        metrics_frame.grid_remove()
        programs_frame.grid_remove()

        metrics_frame.grid(row=0, column=0, sticky="nsew")
        programs_frame.grid(row=1, column=0, sticky="nsew")
