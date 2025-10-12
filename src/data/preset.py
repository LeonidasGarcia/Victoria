class Preset:
    def __init__(
            self,
            name: str = None,
            ram: int = None,
            program_size: int = None,
            page_size: int = None,
            program_count: int = None,
            reference_trace: list[tuple[int, int, int, str]] = [],
            id: int = -1,
    ):
        self.id = id
        self.name = name
        self.ram = ram
        self.program_size = program_size
        self.page_size = page_size
        self.program_count = program_count
        self.reference_trace = reference_trace

    def add_trace(self, pid, page, mode):
        self.reference_trace.append((-1, pid, page, mode))

    def delete_trace(self, trace_id):
        self.reference_trace = [trace for trace in self.reference_trace if trace_id != trace[0]]