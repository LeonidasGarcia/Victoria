import math
import random
from typing import List


def calculate_rows_and_columns(num_elements: int) -> tuple[int, int]:
    columns = round(math.sqrt(num_elements * 3) + 1)
    rows = columns + 1 // 3

    return columns, rows


def gen_hex_colors_list(quantity: int) -> List[str]:
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("La cantidad debe ser un número entero positivo.")

    if quantity > 16777216:
        raise ValueError("La cantidad solicitada excede el número total de colores RGB únicos.")

    unique_colors = set()

    while len(unique_colors) < quantity:
        r = random.randint(0, 16777215)
        hex_color = f'#{r:06x}'
        unique_colors.add(hex_color)

    return list(unique_colors)