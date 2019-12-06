
def add(program, pointer, param_modes):
    x = get_value_in_mode(program, pointer + 1, param_modes[0])
    y = get_value_in_mode(program, pointer + 2, param_modes[1])
    i_out = program[pointer + 3]
    program[i_out] = x + y

    if i_out == pointer:
        return pointer
    return pointer + 4


def multiply(program, pointer, param_modes):
    x = get_value_in_mode(program, pointer + 1, param_modes[0])
    y = get_value_in_mode(program, pointer + 2, param_modes[1])
    i_out = program[pointer + 3]
    program[i_out] = x * y

    if i_out == pointer:
        return pointer
    return pointer + 4


def inp(program, pointer, param_modes):
    x = int(input("Input:").strip())
    i_out = program[pointer + 1]
    program[i_out] = x

    if i_out == pointer:
        return pointer
    return pointer + 2


def out(program, pointer, param_modes):
    print(get_value_in_mode(program, pointer+1, param_modes[0]))
    return pointer + 2


def jump_if_true(program, pointer, param_modes):
    x = get_value_in_mode(program, pointer + 1, param_modes[0])
    y = get_value_in_mode(program, pointer + 2, param_modes[1])
    if x:
        return y
    return pointer + 3


def jump_if_false(program, pointer, param_modes):
    x = get_value_in_mode(program, pointer + 1, param_modes[0])
    y = get_value_in_mode(program, pointer + 2, param_modes[1])
    if not x:
        return y
    return pointer + 3


def less_than(program, pointer, param_modes):
    x = get_value_in_mode(program, pointer + 1, param_modes[0])
    y = get_value_in_mode(program, pointer + 2, param_modes[1])
    i_out = program[pointer + 3]
    program[i_out] = int(x < y)

    if i_out == pointer:
        return pointer
    return pointer + 4


def equals(program, pointer, param_modes):
    x = get_value_in_mode(program, pointer + 1, param_modes[0])
    y = get_value_in_mode(program, pointer + 2, param_modes[1])
    i_out = program[pointer + 3]
    program[i_out] = int(x == y)

    if i_out == pointer:
        return pointer
    return pointer + 4


def get_value_in_mode(program, pointer, mode):
    if mode:
        return program[pointer]
    return program[program[pointer]]


operations2 = {
    1: add, 2: multiply, 3: inp, 4: out, 5: jump_if_true, 6: jump_if_false,
    7: less_than, 8: equals
}


def compute(program):
    pointer = 0
    operator, param_modes = parse_operator(program[pointer])
    while operator != 99:
        pointer = operations2[operator](program, pointer, param_modes)
        operator, param_modes = parse_operator(program[pointer])


def parse_operator(operator):
    opertor_str = str(operator).zfill(5)
    return int(opertor_str[-2:]), (int(opertor_str[2]), int(opertor_str[1]), int(opertor_str[0]))


def modify_two_first_input_positions_and_compute(program, noun, verb):
    program[1] = noun
    program[2] = verb
    compute(program)


def modify_two_first_input_positions_to_get_desired_output(program, desired_output):
    for noun in range(99):
        for verb in range(99):
            program_copy = list(program)
            try:
                modify_two_first_input_positions_and_compute(program_copy, noun, verb)
            except KeyError:
                continue
            if program_copy[0] == desired_output:
                return 100 * noun + verb
    return None


if __name__ == '__main__':
    # with open("../input/int_program.txt") as f:
    #     test_program = list(map(int, f.read().split(",")))
    # test_desired_output = 19690720
    # print(modify_two_first_input_positions_to_get_desired_output(list(test_program), test_desired_output))

    with open("../input/int_program2.txt") as f:
        program_str = f.read()

    # program_str = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    test_program = list(map(int, program_str.split(",")))
    compute(test_program)