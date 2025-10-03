from core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm
from core.constants import FRAME_QUANTITY


class Clk(PageReplacementAlgorithm):
    def __init__(self):
        super().__init__()
        self.resume: int = 0

    def execute_algorithm(self, frame_usage) -> int:
        for i in range(2):
            for fpn in range(self.resume, FRAME_QUANTITY):
                R = frame_usage.loc[fpn, "R"]

                if R == 1:
                    frame_usage.loc[fpn, "R"] = 0
                else:
                    if fpn + 1 >= FRAME_QUANTITY:
                        self.reset()
                    else:
                        self.resume = fpn + 1
                        print("fpn devuelto = ", fpn)
                    return fpn
            self.resume = 0

        raise RuntimeError(
            "Suerte infinita para quien encuentre este error, espero no te agarre en tu exposición asjfaskj"
        )

    def reset(self):
        self.resume = 0
