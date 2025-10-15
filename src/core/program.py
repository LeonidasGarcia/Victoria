import random
from src.core.page_table import PageTable


class Program:
    def __init__(self, pid: int, program_size: int, page_quantity: int, name: str = "generic program", data: str = "d"):
        self.program_size = program_size
        self.page_quantity = page_quantity
        self.pid = pid
        self.name = name
        self.data = data
        self.page_table = PageTable(self.page_quantity)

    def reset_page_table(self):
        self.page_table.reset()

    def generate_memory_request(
            self, vpn: int = -1, mode: str = "r"
    ) -> tuple[int, int, str]:
        if vpn < 0:
            return (
                self.pid,
                random.randint(0, self.page_quantity - 1),
                random.choice(["w", "r"]),
            )

        if vpn >= self.page_quantity:
            raise RuntimeError("Illegal access to virtual memory")

        return (self.pid, vpn, mode)

    def __str__(self):
        return f"Process {self.pid} (data = {self.data})"
