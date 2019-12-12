import pytest
from src.moons import find_total_energy_after_n_steps, find_cycle_time, parse_moons_str
from src.helpers import read


@pytest.mark.parametrize("input_file_num, n_steps, expected_energy, expected_cycle_time", [
    (1, 100, 1940, 4686774924), (2, 1000, 6849, 356658899375688)
])
def test_moons(input_file_num, n_steps, expected_energy, expected_cycle_time):
    moons = parse_moons_str(read(f"moons{input_file_num}.txt"))
    assert find_total_energy_after_n_steps(moons, n_steps) == expected_energy
    assert find_cycle_time(moons) == expected_cycle_time
