from __future__ import annotations
from dataclasses import dataclass, field

from itertools import repeat
from src.helpers import read_line_separated_list


@dataclass
class RecursiveGrid:
    width: int
    height: int
    center: tuple
    levels: dict = field(default_factory=dict)
    memo: dict = field(init=False)

    def __post_init__(self):
        new_level_grid = self.create_new_level_grid()
        state = (tuple(new_level_grid[key] for key in sorted(new_level_grid)), (0, 0, 0, 0), (0, 0, 0, 0))
        self.memo = {state: new_level_grid}

    def update_all(self):
        processed_levels = {}
        for level in set(self.levels) | self.next_levels():
            processed_levels[level] = self.update(level)
        self.levels = processed_levels

    def next_levels(self):
        next_levels = set()
        for level in self.levels:
            if self.affects_inner(level) and level + 1:
                next_levels.add(level + 1)
            if self.affects_outer(level) and level - 1:
                next_levels.add(level - 1)
        return next_levels

    def affects_inner(self, level):
        return any(self.levels[level][move(*self.center)] for move in move_one_step_in_direction.values())

    def affects_outer(self, level):
        return any(self.edge(level, direction) for direction in move_one_step_in_direction)

    def update(self, level):
        state = self.as_tuple(level)
        if state not in self.memo:
            new_grid = dict()
            for pos in self.get_level(level):
                new_grid[pos] = self.get_next_val(level, pos)
            self.memo[state] = new_grid

        return self.memo[state]

    def get_next_val(self, level, pos):
        n_other_bugs = 0
        for direction, move in move_one_step_in_direction.items():
            n_other_bugs += self.get(level, move(*pos), direction)
        if self.get_level(level)[pos]:
            return int(n_other_bugs == 1)
        return int(1 <= n_other_bugs <= 2)

    def edge(self, level, from_direction):
        gen = {
            "R": zip(range(self.height), repeat(0, self.height)),
            "L": zip(range(self.height), repeat(self.width - 1, self.height)),
            "U": zip(repeat(self.height - 1, self.width), range(self.width)),
            "D": zip(repeat(0, self.width), range(self.width))
        }[from_direction]
        grid = self.get_level(level)
        return sum(grid[pos] for pos in gen)

    def get(self, level, pos, from_direction):
        grid = self.levels[level]
        if pos in grid:
            return grid[pos]
        if pos == self.center:
            return self.get_inner(level, from_direction)
        return self.get_outer(level, from_direction)

    def get_outer(self, level, from_direction):
        return self.get_level(level - 1)[move_one_step_in_direction[from_direction](*self.center)]

    def get_inner(self, level, from_direction):
        return self.edge(level + 1, from_direction)

    def as_tuple(self, level):
        if level - 1 in self.levels:
            outer_state = tuple(map(lambda d: self.get_outer(level, d), move_one_step_in_direction))
        else:
            outer_state = (0, 0, 0, 0)

        if level + 1 in self.levels:
            inner_state = tuple(map(lambda d: self.get_inner(level, d), move_one_step_in_direction))
        else:
            inner_state = (0, 0, 0, 0)

        grid = self.get_level(level)
        return tuple(grid[key] for key in sorted(grid)), inner_state, outer_state

    def add_level(self, level, grid=None):
        if grid is None:
            grid = self.create_new_level_grid()
        self.levels[level] = grid

    def create_new_level_grid(self):
        return {(i, j): 0 for i in range(self.height) for j in range(self.width) if (i, j) != self.center}

    def get_level(self, level):
        if level not in self.levels:
            self.add_level(level)
        return self.levels[level]

    def print(self):
        sorted_levels = sorted(self.levels)
        lines = [" | ".join(f"{l}".rjust(self.width) for l in sorted_levels)]
        for i in range(self.height):
            lines_per_level = []
            for l in sorted_levels:
                line_for_level = ""
                for j in range(self.width):
                    if (i, j) in self.levels[l]:
                        line_for_level += "#" if self.levels[l][(i, j)] else "."
                    else:
                        line_for_level += "?"
                lines_per_level.append(line_for_level)
            lines.append(" | ".join(lines_per_level))
        print("\n".join(lines))

    def bio_rating(self, level):
        s = 0
        for i, val in enumerate(self.levels[level].values()):
            if val:
                s += 2 ** i
        return s

move_one_step_in_direction = {
    "R": lambda i, j: (i, j+1),
    "L": lambda i, j: (i, j-1),
    "U": lambda i, j: (i-1, j),
    "D": lambda i, j: (i+1, j)
}

reverse_direction = {"R": "L", "L": "R", "U": "D", "D": "U"}


if __name__ == '__main__':
    inp = read_line_separated_list("bugs2.txt")
    grid_values = {}
    center = None
    for i, line in enumerate(inp):
        for j, c in enumerate(line):
            if c != "?":
                grid_values[(i, j)] = int(c == "#")
            else:
                center = (i, j)

    height = max(grid_values, key=lambda x: x[0])[0] + 1
    width = max(grid_values, key=lambda x: x[1])[1] + 1

    recursive_grid = RecursiveGrid(width, height, center)
    recursive_grid.add_level(0, grid_values)
    recursive_grid.print()

    for i in range(200):
        recursive_grid.update_all()

    s = sum(x for vx in recursive_grid.levels.values() for x in vx.values())
    print(s)


