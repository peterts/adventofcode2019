from src.orbits import (
    read_and_parse_orbit_input, total_number_of_direct_and_indirect_orbits, minimum_number_of_orbital_transfers
)


def test_total_number_of_direct_and_indirect_orbits():
    _orbits = read_and_parse_orbit_input("orbits.txt")
    assert total_number_of_direct_and_indirect_orbits(_orbits) == 247089


def test_minimum_number_of_orbital_transfers():
    _orbits = read_and_parse_orbit_input("orbits2.txt")
    assert minimum_number_of_orbital_transfers(_orbits) == 442
