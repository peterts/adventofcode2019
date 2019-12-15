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


def plot(pixels_defaultdict):
    all_i, all_j = zip(*pixels_defaultdict.keys())
    min_i, min_j = -min(all_i), -min(all_j)
    arr = np.zeros((min_i + max(all_i)+1, min_j + max(all_j)+1))

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i][j] = pixels_defaultdict[(i - min_i, j - min_j)]

    pt.imshow(arr)
    pt.show()


