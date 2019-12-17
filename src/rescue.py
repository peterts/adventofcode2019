from src.helpers import read_comma_separated_list, clean_lines_iter
from src.int_program import IntProgram
import re

move_one_step_in_direction = {
    "R": lambda i, j: (i, j+1),
    "L": lambda i, j: (i, j-1),
    "U": lambda i, j: (i-1, j),
    "D": lambda i, j: (i+1, j)
}

TURN_RIGHT = {"U": "R", "R": "D", "D": "L", "L": "U"}
TURN_LEFT = dict((v, k) for k, v in TURN_RIGHT.items())

SUB_PATH_PATTERN = r"^(.{1,21})\1*(.{1,21})(?:\1|\2)*(.{1,21})(?:\1|\2|\3)*$"


def is_intersection(lines, i, j, n, m):
    if i < 1 or i > n - 2 or j < 1 or j > m - 2:
        return False
    return all(lines[k][l] == "#" for k, l in ((i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)))


def get_scaffold_map(memory):
    program = IntProgram(memory)
    program.run()
    return ''.join(map(chr, program.output))


def get_sum_of_intersection_coord_products(scaffold_map_lines):
    n = len(scaffold_map_lines)
    m = len(scaffold_map_lines[0])

    intersections = []

    for i, line in enumerate(scaffold_map_lines):
        for j, c in enumerate(line):
            if is_intersection(scaffold_map_lines, i, j, n, m):
                intersections.append(i*j)

    return sum(intersections)


def find_robot(scaffold_map_lines):
    for i, line in enumerate(scaffold_map_lines):
        for j, c in enumerate(line):
            if c in ">^v<":
                return i, j
    return None


def get_num_scaffolds(scaffold_map_lines):
    return len(re.findall(f'[{re.escape("#^v<>")}]', ''.join(scaffold_map_lines)))


def get_robot_path(scaffold_map_lines):
    n = len(scaffold_map_lines)
    m = len(scaffold_map_lines[0])

    i, j = find_robot(scaffold_map_lines)

    n_scaffolds = get_num_scaffolds(scaffold_map_lines)

    direction = "UDLR"["^v<>".index(scaffold_map_lines[i][j])]
    visited = {(i, j)}

    operations = []

    def can_move(_direction):
        k, l = move_one_step_in_direction[_direction](i, j)
        return -1 < k < n and -1 < l < m and scaffold_map_lines[k][l] == "#"

    steps = 0

    while len(visited) < n_scaffolds:
        if can_move(direction):
            steps += 1

        else:
            if steps > 0:
                operations.append(steps+1)
            steps = 0

            if can_move(TURN_RIGHT[direction]):
                direction = TURN_RIGHT[direction]
                operations.append("R")

            elif can_move(TURN_LEFT[direction]):
                direction = TURN_LEFT[direction]
                operations.append("L")

            else:
                raise RuntimeError("Something went wrong")

        i, j = move_one_step_in_direction[direction](i, j)
        visited.add((i, j))

    if steps > 0:
        operations.append(steps+1)

    return operations


def get_sub_paths(path):
    path_str = ",".join(map(str, path))
    match = re.match(SUB_PATH_PATTERN, path_str + ",")

    sub_paths = []
    for i in range(1, 4):
        sub_paths.append(match.group(i)[:-1])

    for p, c in zip(sub_paths, ("A", "B", "C")):
        path_str = path_str.replace(p, c)

    return path_str, sub_paths


def path_to_command(path):
    return list(map(ord, path)) + [10]


if __name__ == '__main__':
    memory = read_comma_separated_list("rescue.txt", int)
    program = IntProgram(memory)
    program.run()

    scaffold_map = get_scaffold_map(memory)
    scaffold_map_lines = list(clean_lines_iter(scaffold_map))

    print(get_sum_of_intersection_coord_products(scaffold_map_lines))

    path = get_robot_path(scaffold_map_lines)
    main_path, sub_paths = get_sub_paths(path)

    memory[0] = 2
    program = IntProgram(memory)

    program.run(path_to_command(main_path))
    for sub_path in sub_paths:
        program.run(path_to_command(sub_path))
    program.run([ord('n'), 10])

    print(program.output[-1])
