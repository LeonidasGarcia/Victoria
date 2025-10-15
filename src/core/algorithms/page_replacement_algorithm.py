from typing import Optional

from pandas import DataFrame


# Place Replacement Algorithm
class PageReplacementAlgorithm:
    def __init__(self, frame_quantity: int = 0):
        self.frame_quantity = frame_quantity

    def execute_algorithm(self, frame_usage: DataFrame,
                          next_requests: list[tuple[int, int, str]] | None = None) -> int:
        pass
