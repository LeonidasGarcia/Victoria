from pandas import DataFrame
from src.core.constants import PAGE_QUANTITY

class PageTable:
    def __init__(self):
        self.table = DataFrame(
            {"frame": -1, "valid": False, "dirty": False, "referenced": False},
            index=range(PAGE_QUANTITY),
        )

        self.table.index.name = "VPN"

    def check_dirty(self, vpn):
        try:
            table = self.table
            dirty = table.loc[vpn, "dirty"].tolist()
            return dirty
        except KeyError:
            raise RuntimeError(f"VPN {vpn} out of bounds")

    def check_valid(self, vpn):
        return self.table.loc[vpn, "valid"]

    def link_page(self, vpn, fpn):
        self.table.loc[vpn, :] = [fpn, True, False, True]

    def update_page(self, vpn, dirty=True):
        self.table.loc[vpn, ["dirty"]] = dirty

    def unlink_page(self, vpn):
        try:
            self.table.loc[vpn, ["frame", "valid", "dirty", "referenced"]] = [
                -1,
                False,
                False,
                False,
            ]

        except KeyError:
            raise RuntimeError(
                f"Fallo al desvincular: VPN {vpn} no existe en la tabla."
            )
