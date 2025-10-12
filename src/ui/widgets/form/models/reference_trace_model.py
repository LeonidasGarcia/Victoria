from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from pydantic_core import PydanticCustomError


class ReferenceTraceModel(BaseModel):
    program_count: int = Field(..., title="Program count", description="Conteo de programas")
    page_count: int = Field(..., title="Page count", description="Conteo de paginas")
    pid: int = Field(..., title="Program count", description="ID del programa")
    page: int = Field(..., title="Page", description="Pagina solicitada por el programa")
    mode: str = Field(..., max_length=1, title="Mode", description="Modo de acceso a memoria")

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

    @field_validator('page_count')
    @classmethod
    def check_page_count_gt_zero(cls, value):
        if value <= 0:
            raise PydanticCustomError(
                'valor_no_positivo',
                'La cantidad de páginas debe ser mayor que cero.',
                {'valor': value}
            )
        return value

    @field_validator('pid')
    @classmethod
    def check_pid_gt_zero(cls, value):
        if value <= -1:
            raise PydanticCustomError(
                'valor_no_positivo',
                'El PID no puede ser negativo',
                {'valor': value}
            )
        return value

    @field_validator('page')
    @classmethod
    def check_page_gt_zero(cls, value):
        if value <= -1:
            raise PydanticCustomError(
                'valor_no_positivo',
                'La pagina no puede ser negativa',
                {'valor': value}
            )
        return value

    @model_validator(mode="after")
    @classmethod
    def check_on_bounds(cls, self) -> type["ReferenceTraceModel"]:
        pid = self.pid
        program_max = self.program_count

        if pid >= program_max:
            raise PydanticCustomError(
                "valor_no_valido",
                "El PID ingresado no existe",
                {'valor': pid}
            )

        page = self.page
        page_max = self.page_count

        if page >= page_max:
            raise PydanticCustomError(
                "valor_no_valido",
                "La página ingresada no es válida",
                {'valor': page}
            )

        return self

    @field_validator("pid", mode="before")
    @classmethod
    def check_integer_pid(cls, v):
        if not isinstance(v, int):
            raise PydanticCustomError(
                "valor_no_valido",
                "No se permiten valores decimales en PID",
                {'valor': v}
            )
        return v

    @field_validator("page", mode="before")
    @classmethod
    def check_integer_page(cls, v):
        if not isinstance(v, int):
            raise PydanticCustomError(
                "valor_no_valido",
                "No se permiten valores decimales en la pagina",
                {'valor': v}
            )
        return v

    @field_validator("mode", mode="before")
    @classmethod
    def check_valid_mode(cls, v):
        if not v in ["r", "w"]:
            raise PydanticCustomError(
                "valor_no_valido",
                "El modo ingresado no es valido",
                {'valor': v}
            )
        return v