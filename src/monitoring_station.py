from cmath import phase
from sortedcollections import SortedDict
from math import pi, sqrt
from copy import deepcopy
from src.helpers import read


def angle(v1, v2):
    ang = phase(complex(*v1)) - phase(complex(*v2))
    if ang < 0:
        return 2*pi + ang
    return ang


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def create_asteroid_map(asteroid_map_str):
    asteroid_map = []
    for line in filter(lambda x: x, map(lambda l: l.strip(), asteroid_map_str.splitlines())):
        asteroid_map.append(list(map(lambda c: c == "#", line)))
    return asteroid_map


def get_asteroids(asteroid_map):
    asteroids = []
    for i in range(len(asteroid_map)):
        for j in range(len(asteroid_map[0])):
            if asteroid_map[i][j]:
                asteroids.append((i, j))
    return asteroids


def find_all_detectable_asteroids(asteroid, other_asteroids):
    detectable = SortedDict()
    for other_asteroid in other_asteroids:
        if other_asteroid == asteroid:
            continue
        v = other_asteroid[1] - asteroid[1], asteroid[0] - other_asteroid[0]
        rad = angle((0, 1), v)
        dist = distance(asteroid, other_asteroid)
        if rad not in detectable or dist < distance(asteroid, detectable[rad]):
            detectable[rad] = other_asteroid
    return detectable


def find_detectable_per_asteroid(asteroids):
    detectable_per_asteroid = {}
    for asteroid in asteroids:
        detectable_per_asteroid[asteroid] = find_all_detectable_asteroids(asteroid, asteroids)
    return detectable_per_asteroid


def find_asteroid_with_most_other_detectable_asteroids(asteroid_map):
    asteroids = get_asteroids(asteroid_map)
    detectable_per_asteroid = find_detectable_per_asteroid(asteroids)
    best_asteroid = max(detectable_per_asteroid, key=lambda ast: len(detectable_per_asteroid[ast]))
    return best_asteroid, detectable_per_asteroid[best_asteroid]


def find_nth_destroyed_asteroid(monitoring_asteroid, asteroid_map, n):
    asteroid_map = deepcopy(asteroid_map)
    destroyed = []

    detectable = find_all_detectable_asteroids(monitoring_asteroid, get_asteroids(asteroid_map))
    while detectable:
        for other_asteroid in detectable.values():
            i, j = other_asteroid
            asteroid_map[i][j] = False
            destroyed.append(other_asteroid)
        detectable = find_all_detectable_asteroids(monitoring_asteroid, get_asteroids(asteroid_map))

    return destroyed[n-1]


if __name__ == '__main__':
    _asteroid_map = create_asteroid_map(read("monitoring_station2.txt"))
    _best_asteroid, _detectable = find_asteroid_with_most_other_detectable_asteroids(_asteroid_map)
    print(_best_asteroid, len(_detectable))

    nth_destroyed = find_nth_destroyed_asteroid(_best_asteroid, _asteroid_map, 200)
    print(100*nth_destroyed[1] + nth_destroyed[0])





