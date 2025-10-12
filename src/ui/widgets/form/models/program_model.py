from pyexpat.errors import messages

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from pydantic_core import PydanticCustomError


class ProgramModel(BaseModel):
    program_count: int = Field(..., title="Program count", description="Conteo de programas")

    @field_validator('program_count')
    @classmethod
    def check_program_count_gt_zero(cls, value):
        if value <= 0:
            raise PydanticCustomError(
                'valor_no_positivo',
                'La cantidad de programas debe ser mayor que cero.',
                {'valor': value}
            )
        return value

    @field_validator("program_count", mode="before")
    @classmethod
    def check_integer_program_count(cls, v):
        if not isinstance(v, int):
            raise PydanticCustomError(
                'valor_no_valido',
                'No se permiten numeros decimales en el numero de programas',
                {'valor': v}
            )
        return v