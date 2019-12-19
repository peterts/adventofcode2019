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
        start_x = row.index(1)
        try:
            width = row[start_x:].index(0)
        except ValueError:
            width = 50 - start_x

        if width >= 10 and i >= 9 and x[i-9][start_x + 9] == 1:
            break

    print(start_x * 10000 + i - 9)

    memory = read_comma_separated_list("tractor_beam.txt", int)
    picture = defaultdict(int)

    def get_val_at_xy(x, y):
        if (y, x) not in picture:
            program = IntProgram(memory)
            program.run([x, y])
            picture[(y, x)] = program.output[0]
        return picture[(y, x)]

    for y in range(50):
        for x in range(50):
            picture[(y, x)] = get_val_at_xy(x, y)

    print(sum(picture.values()))
    plot(picture)

    start_x = 0
    width = 1
    y = 99
    while 1:
        x = start_x
        val = get_val_at_xy(x, y)
        while not val:
            x += 1
            val = get_val_at_xy(x, y)
        start_x = x

        x = start_x + width
        val = get_val_at_xy(x, y)
        while val:
            x += 1
            val = get_val_at_xy(x, y)
        width = x - start_x

        if width >= 100 and get_val_at_xy(start_x + 99, y - 99) == 1:
            break

        y += 1

    print(start_x * 10000 + y - 99)
