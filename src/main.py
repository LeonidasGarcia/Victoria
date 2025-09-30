from victoria.Victoria import Victoria

# TODO probar aspectos de la memoria virtual para validar funcionamiento correcto
# ejecutar pruebas controladas

victoria = Victoria()

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
    (program_5.pid, 5),
    (program_4.pid, 4),
    (program_3.pid, 3),
    (program_2.pid, 2),
    (program_5.pid, 5),
    (program_4.pid, 4),
    (program_1.pid, 1),
    (program_2.pid, 2),
]

frame_usage = victoria.ram_manager.frame_usage

for pid, vpn in victoria.requests:
    print(f"pid={pid} vpn={vpn}")
    print(frame_usage)
    print("")
    program = victoria.find_program(pid)
    victoria.access_memory(program, vpn)


print(frame_usage)
print(victoria.ram_manager.ram)
print(victoria.page_failure_count)
