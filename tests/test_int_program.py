import pytest
from src.int_program import IntProgram
from src.helpers import read_comma_separated_list


@pytest.mark.parametrize("memory, memory_after_compute", [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
])
def test_compute(memory, memory_after_compute):
    program = IntProgram(memory, always_move_pointer=True)
    program.run()
    assert program.memory == memory_after_compute


def test_correct_diagnostic_code_after_input():
    memory = read_comma_separated_list("int_program2.txt", int)
    program = IntProgram(memory, always_move_pointer=True)
    program.run([1])
    assert not any(program.output[:-1])  # All 0
    assert program.output[-1] == 7286649


@pytest.mark.parametrize("memory, inp, expected_out", [
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 2, 1),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 2, 1),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4,
      20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 7, 999),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4,
      20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 8, 1000),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4,
      20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 9, 1001),
])
def test_other_programs(memory, inp, expected_out):
    program = IntProgram(memory, always_move_pointer=False)
    program.run([inp])
    assert program.output[-1] == expected_out


def test_correct_diagnostic_code_after_input_2():
    memory = read_comma_separated_list("int_program2.txt", int)
    program = IntProgram(memory, always_move_pointer=False)
    program.run([5])
    assert program.output[-1] == 15724522
