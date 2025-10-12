from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from pydantic_core import PydanticCustomError


class AlgorithmModel(BaseModel):
    lru: bool = Field(..., title="LRU", description="LRU active?")
    fifo: bool = Field(..., title="FIFO", description="FIFO active?")
    nru: bool = Field(..., title="NRU", description="NRU active?")
    clk: bool = Field(..., title="CLK", description="CLK active?")
    optimal: bool = Field(..., title="OPTIMAL", description="OPTIMAL active?")

    @model_validator(mode="after")
    @classmethod
    def check_at_least_one_enabled(cls, self) -> type["AlgorithmModel"]:
        lru = self.lru
        fifo = self.fifo
        nru = self.nru
        clk = self.clk
        optimal = self.optimal

        if not (lru or fifo or nru or clk or optimal):
            raise PydanticCustomError(
                "seleccion_no_valida",
                "Debes seleccionar al menos un algoritmo",
                {'valor': None}
            )
        return self