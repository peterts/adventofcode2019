from itertools import combinations
from collections import defaultdict
import re
from src.helpers import clean_lines_iter
from dataclasses import dataclass, field
from copy import deepcopy
from heapq import heappush


@dataclass
class World:
    keys: set
    doors: set
    passage: dict
    map: list

    def get(self, pos):
        i, j = pos
        return self.map[i][j]

    def is_door(self, pos):
        return pos in self.doors

    def is_key(self, pos):
        return pos in self.keys


@dataclass
class State:
    val: str
    network: dict
    cost: int = 0
    has_keys: list = field(default_factory=list)

    def copy(self):
        return State(
            self.val, deepcopy(self.network), self.cost, list(self.has_keys))

    def __eq__(self, other):
        return self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def get_reachable(self):
        reachable = []
        for other_val in self.network[self.val]:
            if other_val.islower():
                reachable.append(other_val)
            elif other_val.lower() in self.has_keys:
                reachable.append(other_val)
        return reachable


def move_to(state: State, new_val: str, copy=False):
    if copy:
        state = state.copy()

    state.cost += state.network[state.val][new_val]

    if new_val.islower():
        state.has_keys.append(new_val)

    pop_from_network(state.network, state.val)

    state.val = new_val

    return state


def shortest_path(state: State, n_keys):
    if len(state.has_keys) == n_keys:
        if state.cost == 136:
            print(state)
        return state

    reachable = state.get_reachable()

    if len(reachable) == 1:
        return shortest_path(move_to(state, reachable[0]), n_keys)

    else:
        potential_states = []
        for new_val in reachable:
            potential_state = shortest_path(move_to(state, new_val, True), n_keys)
            heappush(potential_states, potential_state)

        return potential_states.pop(0)


def add_edge(network, a, b, cost):
    network[a][b] = cost
    network[b][a] = cost


def pop_from_network(network, a):
    neighbors = network.pop(a)

    for b in neighbors:
        network[b].pop(a)

    for b, c in combinations(neighbors, 2):
        cost = neighbors[b] + neighbors[c]
        if c not in network[b] or network[b][c] > cost:
            add_edge(network, b, c, cost)


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


def create_network(world_map, passages, start: tuple, network=None):
    if network is None:
        network = defaultdict(dict)

    queue = [(start, start, 0)]
    visited = set()

    while queue:
        pos, parent_pos, depth = queue.pop(0)
        visited.add(pos)

        val = _get(world_map, pos)
        if val != "." and (pos != parent_pos):
            add_edge(network, _get(world_map, parent_pos), _get(world_map, pos), depth)
            parent_pos, depth = pos, 0

        for connected_pos in passages[pos]:
            if connected_pos not in visited:
                queue.append((connected_pos, parent_pos, depth + 1))

    return network


def _get(arr, pos):
    i, j = pos
    return arr[i][j]


if __name__ == '__main__':
    _world_map = """
    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################
    """

    _world_map = list(clean_lines_iter(_world_map))
    _start = list(find_x(_world_map, "@"))[0]
    _keys = find_x(_world_map, "[a-z]")
    _doors = find_x(_world_map, "[A-Z]")
    _passages = find_x(_world_map, "[a-zA-Z@.]")
    _passages = parse_passage(_passages)

    network = create_network(_world_map, _passages, _start)
    for _key in _keys:
        network = create_network(_world_map, _passages, _key, network)
    for _door in _doors:
        network = create_network(_world_map, _passages, _door, network)

    state = State('@', network)
    state = shortest_path(state, len(_keys))
    print(state.has_keys)
    print(state.cost)


