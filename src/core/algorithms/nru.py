from core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm
import random


class Nru(PageReplacementAlgorithm):
    def execute_algorithm(self, frame_usage) -> int:
        classes = {0: [], 1: [], 2: [], 3: []}
        filters = [
            (frame_usage["R"] == 0) & (frame_usage["M"] == 0),
            (frame_usage["R"] == 0) & (frame_usage["M"] == 1),
            (frame_usage["R"] == 1) & (frame_usage["M"] == 0),
            (frame_usage["R"] == 1) & (frame_usage["M"] == 1),
        ]
        for i in range(0, 4):
            classes[i] = frame_usage.loc[filters[i]].index.tolist()

        fpn = -1

        for priority in classes.values():
            priority_len = len(priority)
            if priority_len != 0:
                fpn = random.choice(priority)
                break

        if fpn == -1:
            raise RuntimeError("Fatal error on NRU: fpn is -1 wtf dude")

        return fpn
