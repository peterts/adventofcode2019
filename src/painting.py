from src.int_program import IntProgram, STATE_HALTED, STATE_WAITING
from src.helpers import read_comma_separated_list
from collections import defaultdict
import numpy as np
from matplotlib import pylab as pt
from src.helpers import plot_arr


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


if __name__ == '__main__':
    memory = read_comma_separated_list("painting.txt", int)

    program = IntProgram(memory)
    i, j = 0, 0
    direction = "U"
    painting = defaultdict(int)
    painting[(i, j)] = 1

    while program.state != STATE_HALTED:
        program.run([painting[(i, j)]])
        painting[(i, j)] = program.output[0]
        move_left = program.output[1]

        direction = new_direction[(direction, program.output[1])]
        i, j = move_one_step_in_direction[direction](i, j)

    plot_arr(painting)




