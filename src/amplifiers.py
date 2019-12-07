from src.int_program import IntProgram, STATE_HALTED
import itertools
from src.helpers import read_comma_separated_list


def compute_thruster_output(memory, settings):
    amplifiers = []
    prev_out = 0
    for setting in settings:
        amplifier = IntProgram(memory)
        amplifier.run([setting, prev_out])
        prev_out = amplifier.output[-1]
        amplifiers.append(amplifier)

    while any(amp.state != STATE_HALTED for amp in amplifiers):
        for amplifier in amplifiers:
            amplifier.run([prev_out])
            prev_out = amplifier.output[-1]

    return amplifiers[-1].output[-1]


def find_max_thruster_output(program, range_min, range_max):
    max_out = -1

    for setting in itertools.permutations(list(range(range_min, range_max))):
        out = compute_thruster_output(program, setting)
        if out > max_out:
            max_out = out

    return max_out


def _list_to_gen(_list):
    return (i for i in _list)


if __name__ == '__main__':
    program = read_comma_separated_list("thrusters.txt", int)
    print(find_max_thruster_output(program, 0, 5))
    print(find_max_thruster_output(program, 5, 10))




