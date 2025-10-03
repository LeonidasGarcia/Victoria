import random
from core.page_table import PageTable
from core.constants import PROGRAM_SIZE, PAGE_QUANTITY


class Program:
    def __init__(self, pid: int, name: str = "generic program", data: str = "d"):
        self.pid = pid
        self.name = name

        if len(data) != 1:
            raise RuntimeError("Illegal data size. Consider using a single character")

        self.data = data
        self.page_table = PageTable()
        self.virtual_size = PROGRAM_SIZE

    def generate_memory_request(
        self, vpn: int = -1, mode: str = "r"
    ) -> tuple[int, int, str]:
        if vpn < 0:
            return (
                self.pid,
                random.randint(0, PAGE_QUANTITY - 1),
                random.choice(["w", "r"]),
            )

        if vpn >= PAGE_QUANTITY:
            raise RuntimeError("Illegal access to virtual memory")

        return (self.pid, vpn, mode)

    def __str__(self):
        return f"Process {self.pid} (data = {self.data})"
