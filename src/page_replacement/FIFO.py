from page_replacement.PRA import PRA


class FIFO(PRA):
    def execute_algorithm(self, frame_usage):
        return int(frame_usage["load_time"].idxmin())
