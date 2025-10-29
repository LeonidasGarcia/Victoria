import tkinter
import tkinter as tk
from tkinter import Frame, Label, Button, ttk
from tkinter.font import Font
from typing import Optional, List

from src.core.victoria import Victoria
from src.ui.colors import victoria_background, victoria_orange, victoria_lightblue, victoria_green, victoria_pink
from src.ui.widgets.form.models.reference_trace_model import ReferenceTraceModel
from src.util.lib import calculate_rows_and_columns


class VictoriaCell(Frame):
    _BREAKPOINT = 350

    def __init__(self, master, victoria: Victoria, program_count: int, program_colors: List[str],
                 reference_trace: Optional[List[ReferenceTraceModel]] = None, is_wide_layout: bool = True, **kwargs):
        self.recursive_id: Optional[str] = None

        self.victoria: Victoria = victoria
        self.program_count: int = program_count
        self.program_colors: List[str] = program_colors
        self.reference_trace: Optional[List[ReferenceTraceModel]] = reference_trace

        self.victoria_setup()

        self.current_request_label: Optional[Label] = None
        self.cell_frame: Optional[Frame] = None
        self.cells: List[Label] = []

        self.metrics_frame: Optional[Frame] = None
        self.logic_time_label: Optional[Label] = None
        self.page_fault_count_label: Optional[Label] = None
        self.page_fault_rate_label: Optional[Label] = None
        self.average_time_accesses_label: Optional[Label] = None
        self.memory_usage_label: Optional[Label] = None

        self.programs_frame: Optional[Frame] = None

        self.is_wide_layout: bool = is_wide_layout

        super().__init__(master, **kwargs)
        self.configure(bg=victoria_background, padx=10, pady=10)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=10)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)

        tk.Label(self, bg=victoria_background, fg="white", font=Font(family="Sans Serif", weight="bold"),
                 text=type(self.victoria.pra).__name__).grid(row=0, column=0,
                                                             sticky="nsw")

        self.top_frame = tk.Frame(self, bg=victoria_background)
        self.top_frame_setup()
        self.top_frame.grid(row=1, column=0, sticky="nsew")

        tk.Frame(self, bg=victoria_background).grid(row=2, column=0, sticky="nsew", pady=5)

        self.mid_frame = tk.Frame(self, bg=victoria_background)
        self.mid_frame_setup()
        self.mid_frame.grid(row=3, column=0, sticky="nsew")

        tk.Frame(self, bg=victoria_background).grid(row=4, column=0, sticky="nsew", pady=5)

        self.bottom_frame = tk.Frame(self, bg=victoria_background)
        self.bottom_frame_setup()
        self.bottom_frame.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        self.bind("<Configure>", self._check_size)
        self.execute_current_request()

    def paint_metrics(self, current_request_data):
        current_request = current_request_data["current_request"]
        metrics = current_request_data["metrics"]

        self.current_request_label.configure(
            text=f"PID {current_request[0]} accediendo a la pagina {current_request[1]} en modo {current_request[2]}")

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

    def execute_current_request(self):
        current_request_data = self.victoria.get_current_request_data()
        self.victoria.execute_next_request()

        self.paint_metrics(current_request_data=current_request_data)

        self.victoria.current_request += 1

        if self.victoria.execution_should_continue():
            self.recursive_id = self.after(1000, self.execute_current_request)
        else:
            self.current_request_label.configure(
                text="Ejecución finalizada :)")

    def stop_current_request(self):
        if self.recursive_id:
            self.after_cancel(self.recursive_id)
            self.recursive_id = None

    def resume_current_request(self):
        if not self.recursive_id:
            self.execute_current_request()

    def reset_current_request(self):
        if self.recursive_id:
            self.stop_current_request()
        self.victoria.reset_execution()
        self.paint_metrics(self.victoria.get_current_request_data())

    def victoria_setup(self):
        program_count = self.program_count
        reference_trace = self.reference_trace

        for i in range(program_count):
            self.victoria.load_program(pid=i, name=f"program_{i}", data=self.program_colors[i])

        if not self.reference_trace:
            self.victoria.generate_random_requests(50)
            return

        for reference in reference_trace:
            pid = reference.pid
            page = reference.page
            mode = reference.mode

            self.victoria.requests.append((pid, page, mode))

    def top_frame_setup(self):
        top_frame = self.top_frame

        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_rowconfigure(0, weight=1)

        current_request = tk.Label(top_frame, bg=victoria_background, fg="white",
                                   font=Font(family="Sans Serif", size=8, weight="bold"), borderwidth=2, relief="solid")
        current_request.grid(row=0, column=0, sticky="nsew")

        self.current_request_label = current_request

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
                cell = tk.Label(cell_frame, text=current_page_frame, fg="white", borderwidth=1, relief="solid")
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

        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=0)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(1, weight=0)

        metrics_frame = tk.Frame(bottom_frame, bg=victoria_background, padx=5, pady=5)

        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_rowconfigure(2, weight=1)
        metrics_frame.grid_rowconfigure(4, weight=1)
        metrics_frame.grid_rowconfigure(6, weight=1)
        metrics_frame.grid_rowconfigure(8, weight=1)
        metrics_frame.grid_rowconfigure(10, weight=1)

        metrics_frame.grid(row=0, column=0, sticky="ew")

        current_request_data = self.victoria.get_current_request_data()["metrics"]

        tk.Label(metrics_frame, text="Métricas", bg=victoria_background, fg=victoria_orange,
                 font=Font(family="Sans Serif", size=14, weight="bold")).grid(row=0, column=0,
                                                                              sticky="nsw")

        tk.Frame(metrics_frame, bg=victoria_background).grid(row=1, column=0, sticky="nsew", pady=2)

        self.logic_time_label = tk.Label(metrics_frame, text=current_request_data["logic_time"], bg=victoria_background,
                                         fg=victoria_lightblue)
        self.logic_time_label.grid(row=2, column=0, sticky="ew")

        tk.Frame(metrics_frame, bg=victoria_background).grid(row=3, column=0, sticky="nsew", pady=2)

        self.page_fault_count_label = tk.Label(metrics_frame, text=current_request_data["page_fault_count"],
                                               bg=victoria_background,
                                               fg=victoria_green)
        self.page_fault_count_label.grid(row=4, column=0, sticky="ew")

        tk.Frame(metrics_frame, bg=victoria_background).grid(row=5, column=0, sticky="nsew", pady=2)

        self.page_fault_rate_label = tk.Label(metrics_frame, text=current_request_data["page_fault_rate"],
                                              bg=victoria_background,
                                              fg=victoria_pink)
        self.page_fault_rate_label.grid(row=6, column=0, sticky="ew")

        tk.Frame(metrics_frame, bg=victoria_background).grid(row=7, column=0, sticky="nsew", pady=2)

        self.average_time_accesses_label = tk.Label(metrics_frame, text=current_request_data["average_time_access"],
                                                    bg=victoria_background, fg=victoria_orange)
        self.average_time_accesses_label.grid(row=8, column=0, sticky="ew")

        tk.Frame(metrics_frame, bg=victoria_background).grid(row=9, column=0, sticky="nsew", pady=2)

        self.memory_usage_label = tk.Label(metrics_frame, text=current_request_data["memory_usage"],
                                           bg=victoria_background, fg=victoria_lightblue)
        self.memory_usage_label.grid(row=10, column=0, sticky="ew")

        programs_frame = tk.Frame(bottom_frame, height=15, bg=victoria_background)

        programs_frame.grid_columnconfigure(0, weight=1)
        programs_frame.grid_columnconfigure(1, weight=0)
        programs_frame.grid_rowconfigure(0, weight=2)
        programs_frame.grid_rowconfigure(2, weight=8)

        programs_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(programs_frame, text="Programas", bg=victoria_background, fg=victoria_lightblue,
                 font=Font(family="Sans Serif", size=14, weight="bold")).grid(row=0, column=0,
                                                                              columnspan=2,
                                                                              sticky="nsw")

        tk.Frame(programs_frame, bg=victoria_background).grid(row=1, column=0, padx=5, pady=5)

        canvas = tk.Canvas(programs_frame, bg=victoria_background, width=140, height=150)

        canvas.grid_columnconfigure(0, weight=1)
        canvas.grid_rowconfigure(0, weight=1)

        canvas.grid(row=2, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(programs_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        wrapper_program_frame = tk.Frame(canvas, bg=victoria_background)

        wrapper_program_frame.grid_columnconfigure(0, weight=1)

        id_child = canvas.create_window((0, 0), window=wrapper_program_frame, anchor="nw")

        wrapper_program_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(id_child, width=event.width))

        programs = self.victoria.programs

        spaced_row = 0
        for i, program in programs.items():
            program_frame = tk.Frame(wrapper_program_frame, bg=victoria_background, borderwidth=1, relief="solid")

            program_frame.grid_columnconfigure(0, weight=0)
            program_frame.grid_columnconfigure(1, weight=1)
            program_frame.grid_rowconfigure(0, weight=1)

            program_frame.grid(row=spaced_row + i, column=0, sticky="ew")
            tk.Label(program_frame, bg=program.data, width=5, height=2).grid(row=0, column=0)
            tk.Label(program_frame, text=f"PID: {program.pid}", bg=victoria_background, fg="white").grid(row=0,
                                                                                                         column=1,
                                                                                                         sticky="ew")

            tk.Frame(wrapper_program_frame, bg=victoria_background).grid(row=spaced_row + i + 1, column=0,
                                                                         sticky="nsew", padx=5,
                                                                         pady=2)
            spaced_row += 1

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
        bottom_frame.grid_columnconfigure(1, weight=0)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(1, weight=0)

        metrics_frame = self.metrics_frame
        programs_frame = self.programs_frame

        metrics_frame.grid_remove()
        programs_frame.grid_remove()

        metrics_frame.grid(row=0, column=0, sticky="ew")
        programs_frame.grid(row=0, column=1, sticky="ew")

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

        metrics_frame.grid(row=0, column=0, sticky="ew")
        programs_frame.grid(row=1, column=0, sticky="ew")
