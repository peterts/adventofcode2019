from src.helpers import read_line_separated_list


def read_and_parse_orbit_input(file_name):
    return dict(read_line_separated_list(file_name, lambda s: s.split(")")[::-1]))


def total_number_of_direct_and_indirect_orbits(orbits):
    n = 0
    for i in orbits:
        parent_i = i
        while parent_i != "COM":
            n += 1
            parent_i = orbits[parent_i]
    return n


def minimum_number_of_orbital_transfers(orbits):
    number_of_steps_to_ancestor_from_you = {}

    parent_i = "YOU"
    n = 0
    while parent_i != "COM":
        number_of_steps_to_ancestor_from_you[parent_i] = n
        parent_i = orbits[parent_i]
        n += 1

    parent_i = "SAN"
    n = 0
    while parent_i not in number_of_steps_to_ancestor_from_you:
        parent_i = orbits[parent_i]
        n += 1

    return number_of_steps_to_ancestor_from_you[parent_i] + n - 2


if __name__ == '__main__':
    _orbits = read_and_parse_orbit_input("orbits.txt")
    print(total_number_of_direct_and_indirect_orbits(_orbits))

    _orbits2 = read_and_parse_orbit_input("orbits2.txt")
    print(minimum_number_of_orbital_transfers(_orbits2))




