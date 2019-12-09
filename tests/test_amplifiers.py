import pytest
from src.helpers import read_comma_separated_list
from src.amplifiers import find_max_thruster_output


@pytest.mark.parametrize("memory, expected_output", [
    ([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], 43210)
])
def test_find_max_thruster_output1(memory, expected_output):
    assert find_max_thruster_output(memory, 0, 5) == expected_output


@pytest.mark.parametrize("settings_range_min, settings_range_max, expected_output", [
    (0, 5, 914828), (5, 10, 17956613)
])
def test_find_max_thruster_output2(settings_range_min, settings_range_max, expected_output):
    memory = read_comma_separated_list("thrusters.txt", int)
    assert find_max_thruster_output(memory, settings_range_min, settings_range_max) == expected_output
