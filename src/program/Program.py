import random
from pag_table.PagTable import PagTable
from static.Static import PROGRAM_SIZE, PAGE_QUANTITY


class Program:
    def __init__(self, pid: int, name: str = "generic program", data: str = "d"):
        self.pid = pid
        self.name = name

        if len(data) != 1:
            raise RuntimeError("Illegal data size. Consider using a single character")

        self.data = data
        self.page_table = PagTable()
        self.virtual_size = PROGRAM_SIZE

    def generate_memory_request(self, virtual_address: int = -1) -> tuple[int, int]:
        if virtual_address < 0:
            return (self.pid, random.randint(0, PAGE_QUANTITY - 1))

        if virtual_address >= PAGE_QUANTITY:
            raise RuntimeError("Illegal access to virtual memory")

        return (self.pid, virtual_address)

    def __str__(self):
        return f"Process {self.pid} (data = {self.data})"
