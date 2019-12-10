import pytest
from src.helpers import read
from src.monitoring_station import (
    find_nth_destroyed_asteroid, find_asteroid_with_most_other_detectable_asteroids, create_asteroid_map
)


@pytest.mark.parametrize("input_file_num, num_detectable, nth_destroyed", [
    (1, 210, (2, 8)), (2, 267, (9, 13))
])
def test_monitoring_station(input_file_num, num_detectable, nth_destroyed):
    _asteroid_map = create_asteroid_map(read(f"monitoring_station{input_file_num}.txt"))
    _best_asteroid, _detectable = find_asteroid_with_most_other_detectable_asteroids(_asteroid_map)
    assert len(_detectable) == num_detectable

    actual_nth_destroyed = find_nth_destroyed_asteroid(_best_asteroid, _asteroid_map, 200)
    assert actual_nth_destroyed == nth_destroyed
