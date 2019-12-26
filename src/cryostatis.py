from src.helpers import read_comma_separated_list, print_arr
from src.int_program import AsciiProgram, STATE_HALTED
from collections import defaultdict
import re


def parse_doors(output):
    return re.findall("(?<=- )(?:north|south|east|west)", output)


move_one_step_in_direction = {
    "east": lambda i, j: (i, j+1),
    "west": lambda i, j: (i, j-1),
    "north": lambda i, j: (i-1, j),
    "south": lambda i, j: (i+1, j)
}


if __name__ == '__main__':
    memory = read_comma_separated_list("cryostasis.txt", int)
    print(len(memory))
    program = AsciiProgram(memory)

    ship_map = defaultdict(lambda: ".")
    pos = (0, 0)
    ship_map[pos] = "x"

    inp = None
    while 1:
        program.run(inp)
        out = program.parsed_output

        if inp in move_one_step_in_direction and "You can't go that way" not in out:
            ship_map[pos] = "x"
            pos = move_one_step_in_direction[inp](*pos)
            ship_map[pos] = "@"

        doors = parse_doors(out)
        for door in doors:
            other_pos = move_one_step_in_direction[door](*pos)
            if ship_map[other_pos] == ".":
                ship_map[other_pos] = door[0].upper()

        print("\nMap:")
        print_arr(ship_map)

        inp = input(out)

        if inp == "exit":
            break
