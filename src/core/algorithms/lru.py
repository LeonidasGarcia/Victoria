from core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm


class Lru(PageReplacementAlgorithm):
    def execute_algorithm(self, frame_usage) -> int:
        return int(frame_usage["referenced_time"].idxmin())
