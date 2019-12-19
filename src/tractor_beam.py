from src.helpers import read_comma_separated_list, plot, read_line_separated_list
from src.int_program import IntProgram
from collections import defaultdict
import numpy as np


if __name__ == '__main__':
    x = """
        #.......................................
    .#......................................
    ..##....................................
    ...###..................................
    ....###.................................
    .....####...............................
    ......#####.............................
    ......######............................
    .......#######..........................
    ........########........................
    .........#########......................
    ..........#########.....................
    ...........##########...................
    ...........############.................
    ............############................
    .............#############..............
    ..............##############............
    ...............###############..........
    ................###############.........
    ................#################.......
    .................########OOOOOOOOOO.....
    ..................#######OOOOOOOOOO#....
    ...................######OOOOOOOOOO###..
    ....................#####OOOOOOOOOO#####
    .....................####OOOOOOOOOO#####
    .....................####OOOOOOOOOO#####
    ......................###OOOOOOOOOO#####
    .......................##OOOOOOOOOO#####
    ........................#OOOOOOOOOO#####
    .........................OOOOOOOOOO#####
    ..........................##############
    ..........................##############
    ...........................#############
    ............................############
    .............................###########
        """
    from src.helpers import clean_lines_iter
    import sys

    x = clean_lines_iter(x)
    x = list(map(lambda row: list(map(lambda c: int(c != "."), row)), x))

    for i, row in enumerate(x):
        start = row.index(1)
        try:
            width = row[start:].index(0)
        except ValueError:
            width = 50 - start

        if width >= 10 and i >= 9 and x[i-9][start+9] == 1:
            break

    print(start * 10000 + i - 9)

    memory = read_comma_separated_list("tractor_beam.txt", int)
    picture = defaultdict(int)

    s = 0
    for y in range(50):
        for x in range(50):
            program = IntProgram(memory)
            program.run([x, y])
            s += program.output[0]
            picture[(y, x)] = program.output[0]
    print(s)

    plot(picture)

    start = 0
    width = 1
    s = 0
    y = 99
    while 1:
        x = start
        program = IntProgram(memory)
        program.run([x, y])
        out = program.output[0]
        while not out:
            x += 1
            program = IntProgram(memory)
            program.run([x, y])
            out = program.output[0]
        start = x

        x = start + width
        program = IntProgram(memory)
        program.run([x, y])
        out = program.output[0]
        while out:
            j += 1
            program = IntProgram(memory)
            program.run([j, i])
            out = program.output[0]
        width = j - start
        print(start, width)
        break

        for k in range(start, start+width+1):
            picture[(i, k)] = 1

        s += max((min(start+width, 50) - start), 0)

        if width >= 100 and i >= 99 and picture[(i-99, start+99)] == 1:
            break

        print(i)

        i += 1

    print(s)
    print(start, width)

    print(picture[(i-99, start+100)])
    print(picture[(i, start-1)])
    print((i-99) * 10000 + start)

    y = []

    for k in range(i - 99, i+1):
        for l in range(start, start + 100):
            y.append(picture[(k, l)])
            picture[(k, l)] = 2

    # plot(picture)
    print(all(y))
    print(y)
    print(len(y))
    print(sum(y) / len(y))

    #
    # x = read_line_separated_list("tractor_beam2.txt", lambda line: list(map(int, line)))
    # x = np.asarray(x)
    # n = 1
    # for i in range(len(x)):
    #     count_l, count_one = 0, 0
    #     found_one = 0
    #     for j in range(len(x[0])):
    #         found_one |= x[i][j]
    #         if not found_one:
    #             count_l += 1
    #         else:
    #             count_one += x[i][j]
    #     print(count_l, count_one)
