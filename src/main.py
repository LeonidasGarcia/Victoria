from victoria.Victoria import Victoria
from page_replacement.NRU import NRU
from page_replacement.LRU import LRU

# TODO realizar pruebas sobre NRU
# TODO implementar algoritmo second chance

victoria = Victoria(PRA=LRU())

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
    (program_5.pid, 5, "r"),
    (program_4.pid, 4, "w"),
    (program_3.pid, 3, "r"),
    (program_2.pid, 2, "r"),
    (program_5.pid, 5, "w"),
    (program_4.pid, 4, "r"),
    (program_1.pid, 1, "r"),
    (program_2.pid, 2, "w"),
]

frame_usage = victoria.ram_manager.frame_usage

for pid, vpn, mode in victoria.requests:
    print(f"pid={pid} vpn={vpn}")
    print(frame_usage)
    print("")
    program = victoria.find_program(pid)
    victoria.masive_r_reset()
    victoria.access_memory(program, vpn, mode)


print(frame_usage)
print(victoria.ram_manager.ram)
print(victoria.page_failure_count)
