def read_comma_separated_list(input_file_name, cast_to=str):
    return _read_list(input_file_name, ",", cast_to)


def read_line_separated_list(input_file_name, cast_to=str):
    return _read_list(input_file_name, "\n", cast_to)


def _read_list(input_file_name, split_char, cast_to):
    with open(f"../input/{input_file_name}") as f:
        return list(map(cast_to, f.read().strip().split(split_char)))


if __name__ == '__main__':
    print(read_line_separated_list("masses.txt", int))