import numpy as np
from matplotlib import pylab as pt


def read_comma_separated_list(input_file_name, cast_to=str):
    return _read_list(input_file_name, ",", cast_to)


def read_line_separated_list(input_file_name, cast_to=str):
    return _read_list(input_file_name, "\n", cast_to)


def _read_list(input_file_name, split_char, cast_to):
    return list(map(cast_to, read(input_file_name).split(split_char)))


def read(input_file_name):
    with open(f"../input/{input_file_name}") as f:
        return f.read().strip()


def clean_lines_iter(s):
    return filter(lambda x: x, map(lambda x: x.strip(), s.splitlines()))


def print_arr(pixels_defaultdict):
    arr = _create_arr_from_defaultdict(pixels_defaultdict)
    for row in arr:
        for c in row:
            print(c, end="")
        print()


def plot_arr(pixels_defaultdict):
    pt.imshow(np.asarray(_create_arr_from_defaultdict(pixels_defaultdict)))
    pt.show()


def _create_arr_from_defaultdict(pixels_defaultdict):
    all_i, all_j = zip(*pixels_defaultdict.keys())
    min_i, min_j = -min(all_i), -min(all_j)
    n, m = min_i + max(all_i) + 1, min_j + max(all_j) + 1

    arr = []

    for i in range(n):
        row = []
        for j in range(m):
            row.append(pixels_defaultdict[(i - min_i, j - min_j)])
        arr.append(row)

    return arr


def egcd(a, b):
    lastremainder, remainder = abs(a), abs(b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if b < 0 else 1)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('modinv for {} does not exist'.format(a))
    return x % m


if __name__ == '__main__':
    print(modinv(17, 29))
    print(12*3 % 29)