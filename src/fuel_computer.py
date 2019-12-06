from src.helpers import read_line_separated_list


def fuel_required_for_module(mass, total=0, recursive=True):
    required_for_this_mass = max(mass // 3 - 2, 0)
    total += required_for_this_mass
    if recursive and required_for_this_mass > 0:
        return fuel_required_for_module(required_for_this_mass, total)
    return total


def total_fuel_requirement_recursive(masses_of_modules):
    return _total_fuel_requirement(masses_of_modules, True)


def total_fuel_requirement_not_recursive(masses_of_modules):
    return _total_fuel_requirement(masses_of_modules, False)


def _total_fuel_requirement(masses_of_modules, recursive):
    return sum(map(lambda mass: fuel_required_for_module(mass, recursive=recursive), masses_of_modules))


if __name__ == '__main__':
    _masses_of_modules = read_line_separated_list("masses.txt", int)
    print(total_fuel_requirement_not_recursive(_masses_of_modules))
    print(total_fuel_requirement_recursive(_masses_of_modules))

