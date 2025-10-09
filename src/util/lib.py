import math

def calculate_rows_and_columns(num_elements: int) -> tuple[int, int]:
    columns = round(math.sqrt(num_elements * 3) + 1)
    rows = columns + 1 // 3

    return columns, rows