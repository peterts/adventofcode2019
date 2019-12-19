from src.helpers import read_comma_separated_list, plot, read_line_separated_list
from src.int_program import IntProgram
from collections import defaultdict
import numpy as np


if __name__ == '__main__':
    # memory = read_comma_separated_list("tractor_beam.txt", int)
    # picture = defaultdict(int)
    #
    # for i in range(50):
    #     for j in range(50):
    #         program = IntProgram(memory)
    #         program.run([i, j])
    #         picture[(i, j)] = program.output[0]
    #
    # text = ""
    # for i in range(50):
    #     for j in range(50):
    #         text += str(picture[(i, j)])
    #     text += "\n"
    #
    # print(sum(picture.values()))
    # plot(picture)
    #
    # with open("tractor_beam2.txt", "w") as f:
    #     f.write(text)

    x = read_line_separated_list("tractor_beam2.txt", lambda line: list(map(int, line)))
    x = np.asarray(x)
    n = 1
    for i in range(len(x)):
        count_l, count_one = 0, 0
        found_one = 0
        for j in range(len(x[0])):
            found_one |= x[i][j]
            if not found_one:
                count_l += 1
            else:
                count_one += x[i][j]
        print(count_l, count_one)
