from page_replacement.PRA import PRA


class LRU(PRA):
    def execute_algorithm(self, frame_usage) -> int:
        return int(frame_usage["referenced_time"].idxmin())
