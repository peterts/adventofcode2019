from src.helpers import read_comma_separated_list
from src.int_program import IntProgram


def str_to_command(_str):
    return list(map(ord, _str)) + [10]


def print_out(output):
    try:
        print("".join(map(chr, output)), end="")
    except ValueError:
        print(output[-1])


commands = """NOT A J
NOT C T
AND D T
OR T J
WALK"""

commands2 = """NOT C T
AND D T
OR E J
OR H J
AND T J
NOT A T
OR T J
OR B T
OR E T
NOT T T
OR T J
RUN"""


if __name__ == '__main__':
    memory = read_comma_separated_list("springdroid.txt", int)
    program = IntProgram(memory)
    program.run()
    print_out(program.output)

    commands_arr = []
    for line in commands2.splitlines():
        commands_arr.extend(str_to_command(line))

    program.run(commands_arr)
    print_out(program.output)


