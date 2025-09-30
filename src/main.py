from victoria.Victoria import Victoria
from page_replacement.NRU import NRU
from page_replacement.LRU import LRU

# TODO implementar algoritmo second chance
# TODO implementar el memory_usage de manera correcta (terminacion de programas)

victoria = Victoria(PRA=NRU())

program_data = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
]

for i in range(0, 6):
    victoria.load_program(i, f"program {i}", program_data[i])

program_1 = victoria.find_program(1)
program_2 = victoria.find_program(2)
program_3 = victoria.find_program(3)
program_4 = victoria.find_program(4)
program_5 = victoria.find_program(5)

victoria.requests = [
    (program_1.pid, 1, "r"),
    (program_2.pid, 2, "r"),
    (program_3.pid, 3, "r"),
    (program_1.pid, 1, "w"),
    (program_4.pid, 4, "r"),
    (program_2.pid, 2, "r"),
]

victoria.init()
