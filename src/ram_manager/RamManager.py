import numpy as np
from pandas import DataFrame
from static.Static import FRAME_QUANTITY


class RamManager:
    def __init__(self):
        self.ram = np.full(FRAME_QUANTITY, "", dtype="U1")
        self.frame_usage = DataFrame(
            {"pid": -1, "vpn": -1, "load_time": 0, "referenced_time": 0},
            index=range(FRAME_QUANTITY),
        )

        self.frame_usage.index.name = "FPN"

        self.num_frames = FRAME_QUANTITY

    def update_frame(self, fpn, pid, vpn, data, referenced_time, load_time=-1):
        frame_usage = self.frame_usage
        if load_time == -1:
            load_time = frame_usage.loc[fpn, "load_time"]

        frame_usage.loc[fpn, :] = [
            pid,
            vpn,
            load_time,
            referenced_time,
        ]
        self.ram[fpn] = data

    def find_fpn(self, pid, vpn) -> int:
        found_fpn = self.frame_usage.loc[
            (self.frame_usage["pid"] == pid) & (self.frame_usage["vpn"] == vpn)
        ].index.tolist()

        if found_fpn:
            return found_fpn[0]
        else:
            return -1

    def find_vpn(self, fpn) -> tuple[int, int]:
        found_reg = self.frame_usage.loc[fpn, ["pid", "vpn"]]

        if not found_reg.empty:
            return tuple(found_reg.values)
        else:
            raise RuntimeError(f"FPN:{fpn} is not valid")
