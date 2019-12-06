import pytest
from src.int_program import compute, parse_operator


@pytest.mark.parametrize("input_program, output", [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
])
def test_compute(input_program, output):
    compute(input_program)
    assert input_program == output


def test_compute2():
    input_program = [1002, 4, 3, 4, 33]
    compute(input_program)
    assert input_program == [1002, 4, 3, 4, 99]

