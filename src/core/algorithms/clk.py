from typing import Optional

from pandas import DataFrame

from src.core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm


class Clk(PageReplacementAlgorithm):
    def __init__(self):
        super().__init__()
        self.resume: int = 0

    def execute_algorithm(self, frame_usage: DataFrame,
                          next_requests: Optional[list[tuple[int, int, str]]] = None) -> int:
        for i in range(2):
            for fpn in range(self.resume, self.frame_quantity):
                R = frame_usage.loc[fpn, "R"]

                if R == 1:
                    frame_usage.loc[fpn, "R"] = 0
                else:
                    if fpn + 1 >= self.frame_quantity:
                        self.reset()
                    else:
                        self.resume = fpn + 1
                    return fpn
            self.resume = 0

        raise RuntimeError(
            "Este error no deberia ocurrir, proveniente del algoritmo CLK"
        )

    def reset(self):
        self.resume = 0
