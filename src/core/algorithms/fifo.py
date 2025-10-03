from core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm


class Fifo(PageReplacementAlgorithm):
    def execute_algorithm(self, frame_usage):
        return int(frame_usage["load_time"].idxmin())
