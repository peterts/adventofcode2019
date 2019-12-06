move_one_step_in_direction = {
    "R": lambda i, j: (i+1, j),
    "L": lambda i, j: (i-1, j),
    "U": lambda i, j: (i, j+1),
    "D": lambda i, j: (i, j-1)
}


def move(i, j, direction_and_magnitude):
    direction = direction_and_magnitude[0]
    magnitude = int(direction_and_magnitude[1:])
    for _ in range(magnitude):
        i, j = move_one_step_in_direction[direction](i, j)
        yield (i, j)


def get_all_steps_of_path(path):
    position = (0, 0)
    seen = set()
    length = 0
    for direction_and_magnitude in path:
        for position in move(*position, direction_and_magnitude):
            length += 1
            if position not in seen:
                yield position, length
                seen.add(position)


def find_distance_to_closest_point_wires_are_crossing(paths):
    paths = _split_paths(paths)

    wire0_steps = set(position for position, _ in get_all_steps_of_path(paths[0]))

    closest = None
    for position, _ in get_all_steps_of_path(paths[1]):
        if position in wire0_steps:
            dist = abs(position[0]) + abs(position[1])
            if closest is None or dist < closest:
                closest = dist

    return closest


def find_least_number_of_steps_intersection(paths):
    paths = _split_paths(paths)

    wire0_steps = {position: length for position, length in get_all_steps_of_path(paths[0])}

    closest = None
    for position, length1 in get_all_steps_of_path(paths[1]):
        if position in wire0_steps:
            length0 = wire0_steps[position]
            dist = length1 + length0
            if closest is None or dist < closest:
                closest = dist

    return closest


def _split_paths(paths):
    return [p.split(",") for p in paths.splitlines()]


if __name__ == '__main__':
    with open("../input/wires.txt") as f:
        paths = f.read().strip()
    print(find_distance_to_closest_point_wires_are_crossing(paths))
    print(find_least_number_of_steps_intersection(paths))
