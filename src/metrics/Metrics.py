from pandas import DataFrame
from numpy import ndarray
from static.Static import FRAME_QUANTITY


class Metrics:
    def __init__(
        self,
        active: bool = True,
        ram: bool = True,
        page_fault_count: bool = True,
        page_fault_rate: bool = True,
        average_time_access: bool = True,
        memory_usage: bool = True,
    ):
        self.active = active
        self.metrics_to_show: dict[str, bool] = {
            "page_fault_count": page_fault_count,
            "page_fault_rate": page_fault_rate,
            "average_time_access": average_time_access,
            "memory_usage": memory_usage,
        }
        self.ram_history: list[tuple] = []

    def add_ram_log(
        self,
        frame_usage: DataFrame,
        ram: ndarray,
        total_faults: int,
        clock: int,
        total_accesses: int,
        busy_frames: int,
    ):
        self.ram_history.append(
            {
                "frame": frame_usage.to_string(),
                "ram": str(ram),
                "page_fault_count": "Page failure count: " + str(total_faults),
                "page_fault_rate": "Page failure rate: "
                + str(round((total_faults / total_accesses) * 100, 2))
                + "%",
                "average_time_access": "Average time access in memory: "
                + str(round(clock / total_accesses, 2)),
                "memory_usage": "Memory usage: "
                + str(round((busy_frames / FRAME_QUANTITY) * 100, 2))
                + "%",
            }
        )

    def print_log(self, log: dict):
        print(log["frame"])
        print(log["ram"])
        print("")
        for field in self.metrics_to_show.keys():
            print(log[field])
        print("\n")

    def print_step_by_step(self):
        if not self.active:
            return
        for log in self.ram_history:
            self.print_log(log)

    def print_final_results(self):
        if not self.active:
            return
        self.print_log(self.ram_history[-1])
