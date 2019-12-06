import pytest
from src.helpers import read_line_separated_list
from src.fuel_computer import total_fuel_requirement_recursive, total_fuel_requirement_not_recursive


@pytest.fixture(scope="module")
def masses_of_modules():
    return read_line_separated_list("masses.txt", int)


@pytest.mark.parametrize("compute_func, output", [
    (total_fuel_requirement_not_recursive, 3267890),
    (total_fuel_requirement_recursive, 4898972)
])
def test_compute_fuel_requirements(compute_func, output, masses_of_modules):
    assert compute_func(masses_of_modules) == output
