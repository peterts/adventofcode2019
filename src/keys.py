from src.helpers import clean_lines_iter
import re
from collections import defaultdict
from heapq import heappush
from dataclasses import dataclass, field


@dataclass
class World:
    keys: list
    doors: list
    passage: dict
    map: list

    def get(self, pos):
        i, j = pos
        return self.map[i][j].lower()


@dataclass
class State:
    pos: tuple
    cost: int = 0
    has_keys: tuple = field(default_factory=tuple)
    opened_doors: tuple = field(default_factory=tuple)

    def add_key_and_copy(self, key_pos, key_val, cost):
        return State(key_pos, self.cost + cost, (*self.has_keys, key_val), self.opened_doors)

    def add_door_and_copy(self, door_pos, door_val, cost):
        return State(door_pos, self.cost + cost, self.has_keys, (*self.opened_doors, door_val))

    def __eq__(self, other):
        return self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost


def find_x(world_map, x):
    found = []
    for i, line in enumerate(world_map):
        for match in re.finditer(x, line):
            found.append((i, match.start()))
    return found


def shortest_path(world: World, state: State):
    if len(state.has_keys) == len(world.keys):
        return state

    new_keys, doors_that_can_be_opened = search(world, state)

    if (len(new_keys) + len(doors_that_can_be_opened)) == 1:
        if new_keys:
            key_dist, key = new_keys.pop(0)
            return shortest_path(world, state.add_key_and_copy(key, world.get(key), key_dist))
        else:
            door_dist, door = doors_that_can_be_opened.pop(0)
            return shortest_path(world, state.add_door_and_copy(door, world.get(door), door_dist))

    else:
        costs = []
        for key_dist, key in new_keys:
            potential_state = shortest_path(world, state.add_key_and_copy(key, world.get(key), key_dist))
            heappush(costs, potential_state)

        for door_dist, door in doors_that_can_be_opened:
            potential_state = shortest_path(world, state.add_door_and_copy(door, world.get(door), door_dist))
            heappush(costs, potential_state)

        return costs.pop(0)


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


def search(world: World, state: State):
    new_keys = []
    doors_that_can_be_opened = []
    visisted = set()

    queue = [(state.pos, 0)]

    while queue:
        pos, dist = queue.pop(0)
        visisted.add(pos)

        if pos in world.doors:
            door = world.get(pos)
            if door not in state.has_keys:
                continue
            elif door not in state.opened_doors:
                heappush(doors_that_can_be_opened, (dist, pos))
                continue

        elif pos in world.keys:
            if world.get(pos) not in state.has_keys:
                heappush(new_keys, (dist, pos))
                continue

        for connected_pos in world.passage[pos]:
            if connected_pos in visisted:
                continue
            queue.append((connected_pos, dist+1))

    return new_keys, doors_that_can_be_opened


if __name__ == '__main__':
    _map = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
    """
    _map = list(clean_lines_iter(_map))
    _door = find_x(_map, "@")[0]

    _keys = find_x(_map, "[a-z]")

    _doors = find_x(_map, "[A-Z]")

    _passage = find_x(_map, "[a-zA-Z@.]")
    _passage = parse_passage(_passage)

    world = World(_keys, _doors, _passage, _map)
    state = State(_door)

    print(shortest_path(world, state))
