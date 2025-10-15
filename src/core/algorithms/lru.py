from typing import Optional

from pandas import DataFrame

from src.core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm


class Lru(PageReplacementAlgorithm):
    def execute_algorithm(self, frame_usage: DataFrame,
                          next_requests: Optional[list[tuple[int, int, str]]] = None) -> int:
        return int(frame_usage["referenced_time"].idxmin())
