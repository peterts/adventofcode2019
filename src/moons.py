from dataclasses import dataclass, field
import numpy as np
import re
from copy import deepcopy
import math
from src.helpers import read

@dataclass
class Moon:
    position: np.ndarray
    velocity: np.ndarray = field(default_factory=lambda: np.asarray([0, 0, 0]))
    velocity_update: np.ndarray = field(default_factory=lambda: np.asarray([0, 0, 0]))

    def update(self):
        self.velocity += self.velocity_update
        self.position += self.velocity
        self.velocity_update = np.asarray([0, 0, 0])

    def apply_gravity(self, other):
        inc = (self.position < other.position).astype(int)
        dec = (self.position > other.position).astype(int)
        self.velocity_update += (inc - dec)

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


def is_repeat(moons, initial_moons, i):
    return all(old_moon.position[i] == moon.position[i] for old_moon, moon in zip(moons, initial_moons)) and \
        all(old_moon.velocity[i] == moon.velocity[i] for old_moon, moon in zip(moons, initial_moons))


def find_total_energy_after_n_steps(moons, n):
    moons = deepcopy(moons)
    for _ in range(n):
        step(moons)
    return sum(moon.energy() for moon in moons)


def find_cycle_time(moons):
    moons = deepcopy(moons)
    original_moons = deepcopy(moons)
    t = 0
    phases = [0] * 3
    while not all(phases):
        step(moons)
        t += 1
        for i in range(3):
            if phases[i]:
                continue
            if is_repeat(moons, original_moons, i):
                phases[i] = t
    return lcm(phases)


def parse_moons_str(moons_str):
    moons = []
    for moon_str in filter(lambda x: x, map(lambda x: x.strip(), moons_str.splitlines())):
        moons.append(create_moon(moon_str))
    return moons


if __name__ == '__main__':
    moons_str = read("moons2.txt")
    moons = parse_moons_str(moons_str)
    print(find_total_energy_after_n_steps(moons, 1000))
    print(find_cycle_time(moons))


