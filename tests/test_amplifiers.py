import pytest
from src.helpers import read_comma_separated_list
from src.amplifiers import find_max_thruster_output


@pytest.mark.parametrize("settings_range_min, settings_range_max, expected_output", [
    (0, 5, 914828), (5, 10, 17956613)
])
def test_find_max_thruster_output(settings_range_min, settings_range_max, expected_output):
    memory = read_comma_separated_list("thrusters.txt", int)
    assert find_max_thruster_output(memory, settings_range_min, settings_range_max) == expected_output
