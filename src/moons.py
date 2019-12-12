from dataclasses import dataclass, field
import numpy as np
import re
from copy import deepcopy, copy
import math


def arr_is_in(arr, arr_list):
    return any(np.array_equal(arr, arr2) for arr2 in arr_list)


@dataclass
class Moon:
    position: np.ndarray
    velocity: np.ndarray = np.asarray([0, 0, 0])
    velocity_update: np.ndarray = np.asarray([0, 0, 0])
    history: list = field(default_factory=list)
    phase: float = -1

    def update(self):
        self.velocity = np.add(self.velocity, self.velocity_update)
        self.position = np.add(self.position, self.velocity)
        self.velocity_update = np.asarray([0, 0, 0])

    def apply_gravity(self, other):
        inc = (self.position < other.position).astype(int)
        dec = (self.position > other.position).astype(int)
        self.velocity_update = np.add(self.velocity_update, np.subtract(inc, dec))

    def energy(self):
        potential = np.sum(np.abs(self.position))
        kinetic = np.sum(np.abs(self.velocity))
        return potential * kinetic

    def __eq__(self, other):
        return np.array_equal(self.velocity, other.velocity) and \
               np.array_equal(self.position, other.position)

    def __copy__(self):
        return Moon(np.copy(self.position), np.copy(self.velocity))


def create_moon(s):
    match = re.search(r"<x=(?P<x>-?\d+),\s+y=(?P<y>-?\d+),\s+z=(?P<z>-?\d+)>", s)
    return Moon(np.asarray([
        float(match.group("x")),
        float(match.group("y")),
        float(match.group("z"))
    ]))


def lcm(a):
    _lcm = a[0]
    for x in a[1:]:
        _lcm = (_lcm * x) // math.gcd(_lcm, x)
    return _lcm


def step(moons):
    for i, moon in enumerate(moons):
        for j, other_moon in enumerate(moons):
            if i == j:
                continue
            moon.apply_gravity(other_moon)

    for moon in moons:
        moon.update()


def is_repeat(moons, history, i):
    for old_moons in history:
        if all(old_moon.position[i] == moon.position[i] for old_moon, moon in zip(moons, old_moons)) and \
                all(old_moon.velocity[i] == moon.veolicty[i] for old_moon, moon in zip(moons, old_moons)):
            return True
    return False


if __name__ == '__main__':
    moons_str = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
    """

    moons = []
    for moon_str in filter(lambda x: x, map(lambda x: x.strip(), moons_str.splitlines())):
        moons.append(create_moon(moon_str))

    old_moons = deepcopy(moons)

    t = 0
    history = []

    while moons not in history:
        history.append(deepcopy(moons))
        step(moons)
        # print(f"\r{t}", end="")
        t += 1

    print()
    print(t)
    print(lcm([int(moon.phase) for moon in moons]))

