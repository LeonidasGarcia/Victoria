import random
from typing import Optional

from pandas import DataFrame

from src.core.algorithms.page_replacement_algorithm import PageReplacementAlgorithm


class Optimal(PageReplacementAlgorithm):
    def execute_algorithm(self, frame_usage: DataFrame,
                          next_requests: Optional[list[tuple[int, int, str]]] = None) -> int:
        print("ejecutando optimal")
        current_active_frame = frame_usage[["FPN", "pid", "vpn"]].values.tolist()

        if len(next_requests) == 0:
            return random.randint(0, len(current_active_frame) - 1)

        fpn_target = -1
        current_steps = -1
        for fpn, pid, vpn in current_active_frame:
            is_found = False
            for index, next_request in enumerate(next_requests):
                next_pid = next_request[0]
                next_vpn = next_request[1]

                if pid == next_pid and vpn == next_vpn:
                    if current_steps < index:
                        fpn_target = fpn
                        current_steps = index
                    is_found = True
                    break

            if not is_found:
                return fpn

        return fpn_target
