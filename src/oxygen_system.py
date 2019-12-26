from src.helpers import read_comma_separated_list, plot_arr
from collections import defaultdict
from heapq import heappush
from src.int_program import IntProgram
from math import sqrt


move_one_step_in_direction = {
    4: lambda i, j: (i, j+1),
    3: lambda i, j: (i, j-1),
    1: lambda i, j: (i-1, j),
    2: lambda i, j: (i+1, j)
}


WALL = 0
EMPTY = 1
TARGET = 2
UNKNOWN = 3


def go_to(i, j, path):
    for move in path:
        i, j = move_one_step_in_direction[move](i, j)
    return i, j


def get_all_moves_to_unknown_positions(i, j, path, world):
    options = []

    for move in move_one_step_in_direction:
        new_pos = move_one_step_in_direction[move](i, j)
        if world[new_pos] == UNKNOWN:
            options.append(path + [move])

    return options


def create_map_of_area(memory, return_shortest_path_when_found):
    world = defaultdict(lambda: UNKNOWN)
    shortest_path = None

    queue = [[]]

    while queue:
        program = IntProgram(memory)
        path = queue.pop(0)
        i, j = go_to(0, 0, path)

        if path:
            program.run(path)
            status = program.output[-1]
        else:
            status = EMPTY

        world[(i, j)] = status

        if status == TARGET:
            if shortest_path is None:
                shortest_path = path
                if return_shortest_path_when_found:
                    return world, shortest_path

        if status in (EMPTY, TARGET):
            queue.extend(get_all_moves_to_unknown_positions(i, j, path, world))

    return world, shortest_path


def get_longest_path(world, start_pos):
    queue = [(start_pos, 0)]
    visited = set()
    max_depth = -1
    while queue:
        pos, depth = queue.pop(0)
        if depth > max_depth:
            max_depth = depth
        visited.add(pos)
        for move in move_one_step_in_direction:
            new_pos = move_one_step_in_direction[move](*pos)
            if (world[new_pos] in (EMPTY, TARGET)) and (new_pos not in visited):
                queue.append((new_pos, depth+1))
    return max_depth


if __name__ == '__main__':
    memory = read_comma_separated_list("oxygen_system.txt", int)
    program = IntProgram(memory)

    world, shortest_path = create_map_of_area(memory, False)
    start_pos = go_to(0, 0, shortest_path)

    plot_arr(world)
    print(len(shortest_path))
    print(get_longest_path(world, start_pos))






