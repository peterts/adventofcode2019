from src.helpers import read_line_separated_list
import numpy as np
from matplotlib import pylab as pt


if __name__ == '__main__':
    image = read_line_separated_list("image.txt")[0]
    width = 25
    height = 6

    n_layers = len(image) // (width * height)

    layers = []
    n = 0

    min_num_zero = 1e9
    num_one, num_two = None, None

    for _ in range(n_layers):
        layers.append([])
        num_zero = 0
        for j in range(height):
            layers[-1].append(image[n:n+width])
            num_zero += layers[-1][-1].count("0")
            n += width

        if num_zero < min_num_zero:
            min_num_zero = num_zero
            num_one, num_two = 0, 0
            for row in layers[-1]:
                num_one += row.count("1")
                num_two += row.count("2")

    decoded_image = []

    for i in range(height):
        row = []
        for j in range(width):
            for layer in layers:
                if layer[i][j] == "2":
                    continue
                else:
                    row.append(int(layer[i][j]))
                    break
            else:
                row.append(2)

        decoded_image.append(row)

    img = np.asarray(decoded_image)
    pt.imshow(img)
    pt.show()
