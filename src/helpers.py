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
