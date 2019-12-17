from src.helpers import read_comma_separated_list, clean_lines_iter
from src.int_program import IntProgram
from itertools import chain
from collections import Counter
import re


def is_intersection(lines, i, j, n, m):
    if i < 1 or i > n - 2 or j < 1 or j > m - 2:
        return False
    return all(lines[k][l] == "#" for k, l in ((i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)))


new_direction = {
    ("U", 0): "L", ("U", 1) : "R",
    ("D", 0): "R", ("D", 1): "L",
    ("R", 0): "U", ("R", 1): "D",
    ("L", 0): "D", ("L", 1): "U",
}

move_one_step_in_direction = {
    "R": lambda i, j: (i, j+1),
    "L": lambda i, j: (i, j-1),
    "U": lambda i, j: (i-1, j),
    "D": lambda i, j: (i+1, j)
}

TURN_RIGHT = {"U": "R", "R": "D", "D": "L", "L": "U"}
TURN_LEFT = dict((v, k) for k, v in TURN_RIGHT.items())


def can_move(lines, i, j, direction):
    k, l = move_one_step_in_direction[direction](i, j)
    return -1 < k < n and -1 < l < m and lines[k][l] == "#"


# def split_operations(operations_str, seq):
#     prev_match = None
#     splits = []
#     for match in re.finditer(f"(?=({seq}))", operations_str):
#         if prev_match is not None:
#         pass


def to_command(func):
    print(len(','.join(re.findall(r"(?:[A-Z]|\d+)", func))))
    return list(map(ord, ','.join(re.findall(r"(?:[A-Z]|\d+)", func)))) + [10]


if __name__ == '__main__':
    memory = read_comma_separated_list("rescue.txt", int)
    program = IntProgram(memory)
    program.run()
    s = ''.join(map(chr, program.output))

    lines = list(clean_lines_iter(s))
    n = len(lines)
    m = None

    intersections = []

    robot_or_scaffold = "#>^v<"

    robot = None
    n_scaffolds = 0

    for i, line in enumerate(lines):
        if m is None:
            m = len(line)
        for j, c in enumerate(line):
            if lines[i][j] in robot_or_scaffold:
                n_scaffolds += 1
                if robot_or_scaffold.index(lines[i][j]) > 0:
                    robot = (i, j)

            if is_intersection(lines, i, j, n, m):
                intersections.append(i*j)

    print(n_scaffolds)
    print(s)

    i, j = robot
    direction = "UDLR"["^v<>".index(lines[i][j])]
    visited = {(i, j)}

    operations = []

    steps = 0
    while len(visited) < n_scaffolds:
        if can_move(lines, i, j, direction):
            steps += 1
        else:
            if steps > 0:
                operations.append(steps+1)
            steps = 0

            if can_move(lines, i, j, TURN_RIGHT[direction]):
                direction = TURN_RIGHT[direction]
                operations.append("R")
            elif can_move(lines, i, j, TURN_LEFT[direction]):
                direction = TURN_LEFT[direction]
                operations.append("L")
            else:
                direction = TURN_RIGHT[TURN_RIGHT[direction]]
                operations.append("R")
                operations.append("R")

        i, j = move_one_step_in_direction[direction](i, j)
        visited.add((i, j))

    if steps > 0:
        operations.append(steps+1)
    steps = 0

    operations_str = ' '.join(''.join(map(str, x)) for x in zip(operations[::2], operations[1::2]))

    memory[0] = 2
    program = IntProgram(memory)

    A = "L6 R12 L6 L8 L8"
    B = "L4 L4 L6"
    C = "L6 R12 R8 L8"

    print(operations_str)
    operations_str = operations_str.replace(A, "A")
    print(operations_str)
    operations_str = operations_str.replace(B, "B")
    print(operations_str)
    operations_str = operations_str.replace(C, "C")
    print(operations_str)

    program.memory[0] = 2
    print(program.state)

    program.run(to_command(operations_str))
    print(program.state)
    program.run(to_command(A))
    print(program.state)
    program.run(to_command(B))
    print(program.state)
    program.run(to_command(C))
    print(program.state)
    program.run([ord('n'), 10])
    print(program.state)
    print(program.output)

