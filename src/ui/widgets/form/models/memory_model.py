from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from pydantic_core import PydanticCustomError


class MemoryModel(BaseModel):
    ram: int = Field(..., title="RAM", description="RAM disponible para la simulación")
    program_size: int = Field(..., title="Program size", description="Tamaño de los programas")
    page_size: int = Field(..., title="Page size", description="Tamaño de la página y los marcos de página")

    @field_validator('ram')
    @classmethod
    def check_ram_gt_zero(cls, value):
        if value <= 0:
            raise PydanticCustomError(
                'valor_no_positivo',
                'La cantidad de RAM debe ser mayor que cero.',
                {'valor': value}
            )
        return value

    @field_validator('program_size')
    @classmethod
    def check_program_size_gt_zero(cls, value):
        if value <= 0:
            raise PydanticCustomError(
                'valor_no_positivo',
                'El tamaño del programa debe ser mayor que cero.',
                {'valor': value}
            )
        return value

    @field_validator('page_size')
    @classmethod
    def check_page_size_gt_zero(cls, value):
        if value <= 0:
            raise PydanticCustomError(
                'valor_no_positivo',
                'El tamaño de la pagina debe ser mayor que cero.',
                {'valor': value}
            )
        return value

    @model_validator(mode="after")
    @classmethod
    def check_multiple_of_page_size(cls, self) -> type["MemoryModel"]:
        ram = self.ram
        program_size = self.program_size
        page_size = self.page_size

        mod_ram = ram % page_size
        mod_program_size = program_size % page_size

        if not (mod_ram == 0 and mod_program_size == 0):
            raise PydanticCustomError(
                "valor_no_valido",
                "El tamaño de la página debe ser un divisor entero del RAM y del tamaño del programa",
                {'valor': page_size}
            )

        return self

    @field_validator("ram", mode="before")
    @classmethod
    def check_integer_ram(cls, v):
        if not isinstance(v, int):
            raise PydanticCustomError(
                "valor_no_valido",
                "No se permiten valores decimales en RAM",
                {'valor': v}
            )
        return v

    @field_validator("program_size", mode="before")
    @classmethod
    def check_integer_program_size(cls, v):
        if not isinstance(v, int):
            raise PydanticCustomError(
                "valor_no_valido",
                "No se permiten valores decimales en el tamaño del programa",
                {'valor': v}
            )
        return v

    @field_validator("page_size", mode="before")
    @classmethod
    def check_integer_page_size(cls, v):
        if not isinstance(v, int):
            raise PydanticCustomError(
                "valor_no_valido",
                "No se permiten valores decimales en el tamaño de pagina",
                {'valor': v}
            )
        return v