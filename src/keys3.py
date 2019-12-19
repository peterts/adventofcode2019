import re
from collections import defaultdict
from src.helpers import clean_lines_iter
from dataclasses import dataclass, field
from heapq import heappush


def find_x(world_map, x):
    found = []
    for i, line in enumerate(world_map):
        for match in re.finditer(x, line):
            found.append((i, match.start()))
    return set(found)


def parse_passage(passage):
    parsed_passage = defaultdict(set)

    for pos in passage:
        for other_pos in passage:
            if is_connected(pos, other_pos):
                parsed_passage[pos].add(other_pos)

    return parsed_passage


def is_connected(pos, other_pos):
    return ((pos[0] == other_pos[0]) and abs(pos[1] - other_pos[1]) == 1) or \
           ((pos[1] == other_pos[1]) and abs(pos[0] - other_pos[0]) == 1)


def shortest_path(start, passages, world_map):
    visited = set()
    paths = dict()
    queue = [(start, 0, ())]

    while queue:
        pos, dist, obstacles = queue.pop(0)
        visited.add(pos)

        val = _get(world_map, pos)
        if val.islower() or val == "@":
            paths[val] = (dist, obstacles)
        elif val.isupper():
            obstacles = (*obstacles, val.lower())

        for other_pos in passages[pos]:
            if other_pos in visited:
                continue
            queue.append((other_pos, dist+1, obstacles))

    start_val = _get(world_map, start)
    paths.pop(start_val)
    return {start_val: paths}


def _get(arr, pos):
    i, j = pos
    return arr[i][j]


INF = 1e9


@dataclass(eq=True, frozen=True)
class Node:
    val: str
    keys: tuple = field(default_factory=frozenset)
    lowest_cost: int = field(compare=False, default_factory=lambda: INF)

    def copy_replace_cost(self, new_cost):
        return Node(self.val, self.keys, new_cost)

    def copy_and_add_own_val(self):
        if self.val in self.keys:
            return self
        return Node(self.val, (*self.keys, self.val), self.lowest_cost)

    def __lt__(self, other):
        return self.lowest_cost < other.lowest_cost


def get_final_shortest_path(all_shortest_paths, start_val):
    visited = set()

    min_dist = defaultdict(lambda: (INF, ()))
    queue = [(0, start_val, ())]

    while queue:
        dist, val, path = queue.pop(0)
        visited.add(val)

        path = (*path, val)

        for other_val, (_dist, obstacles) in all_shortest_paths[val].items():
            if any(x not in path for x in obstacles):
                print(other_val, _dist, obstacles, path)
                continue
            if other_val in visited:
                continue

            prev_cost, _ = min_dist[other_val]
            new_cost = dist + _dist

            if new_cost < prev_cost:
                min_dist[other_val] = (new_cost, path)
                heappush(queue, (new_cost, other_val, path))

    return min_dist


if __name__ == '__main__':
    world_map = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
    """
    world_map = list(clean_lines_iter(world_map))
    _door = list(find_x(world_map, "@"))[0]
    _keys = find_x(world_map, "[a-z]")
    _doors = find_x(world_map, "[A-Z]")
    _passage = find_x(world_map, "[a-zA-Z@.]")
    _passage = parse_passage(_passage)

    sp = shortest_path(_door, _passage, world_map)
    for k in _keys:
        sp.update(shortest_path(k, _passage, world_map))

    spf = get_final_shortest_path(sp, '@')
    print(spf)
    print(min(filter(lambda x: len(x[1]) == len(_keys) + 1, spf), key=lambda x: x[0]))

