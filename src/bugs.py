from collections import defaultdict
from src.helpers import read_line_separated_list, clean_lines_iter


def get_next_val(pos, grid):
    n_other_bugs = 0
    for move in move_one_step_in_direction.values():
        n_other_bugs += grid[move(*pos)]
    if grid[pos]:
        return n_other_bugs == 1
    return 1 <= n_other_bugs <= 2


def update(grid):
    new_grid = defaultdict(bool)
    for pos in dict(grid):
        new_grid[pos] = get_next_val(pos, grid)
    return new_grid


def run_and_check_for_duplicate(grid):
    memo = set()
    grid_tup = grid_to_tuple(grid)
    while grid_tup not in memo:
        memo.add(grid_tup)
        grid = update(grid)
        grid_tup = grid_to_tuple(grid)
    return grid


def grid_to_tuple(grid):
    return tuple(map(lambda key: grid[key], sorted(grid)))


def print_grid(grid, n, m):
    for i in range(n):
        for j in range(m):
            val = "#" if grid[(i, j)] else "."
            print(val, end="")
        print()
    print()


move_one_step_in_direction = {
    "R": lambda i, j: (i, j+1),
    "L": lambda i, j: (i, j-1),
    "U": lambda i, j: (i-1, j),
    "D": lambda i, j: (i+1, j)
}


if __name__ == '__main__':
    inp = read_line_separated_list("bugs.txt")
    grid = defaultdict(bool)
    for i, line in enumerate(inp):
        for j, c in enumerate(line):
            grid[(i, j)] = c == "#"

    grid = run_and_check_for_duplicate(grid)

    s = 0
    for i, val in enumerate(grid.values()):
        if val:
            s += 2**i
    print(s)
