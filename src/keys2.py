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
        return sorted(reachable, key=lambda _other_val: self.network[self.val][_other_val])


def move_to(state: State, new_val: str, copy=False):
    if copy:
        state = state.copy()

    state.cost += state.network[state.val][new_val]

    if new_val.islower():
        state.has_keys.append(new_val)

    pop_from_network(state.network, state.val)

    state.val = new_val

    return state


best_state = None


def shortest_path(state: State, n_keys):
    global best_state

    if best_state is not None and state.cost >= best_state.cost:
        return True

    if len(state.has_keys) == n_keys and (best_state is None or state.cost < best_state.cost):
        best_state = state
        print(best_state.cost)
        return True

    reachable = state.get_reachable()
    for new_val in reachable:
        do_break = shortest_path(move_to(state, new_val, True), n_keys)
        if do_break:
            break

    return False


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


def find_shortest_path(network, start):
    visited = set()
    queue = [Node(start, lowest_cost=0)]

    while queue:
        node = queue.pop(0)
        if node.val.islower():
            node = node.copy_and_add_own_val()

        if node not in visited:
            visited.add(node)

            for neighbor_val in get_reachable(network, node.val, node.keys):
                neighbor_node = Node(neighbor_val, node.keys)

                if neighbor_node in visited:
                    continue

                prev_cost = neighbor_node.lowest_cost
                new_cost = node.lowest_cost + network[node.val][neighbor_val]

                if new_cost < prev_cost:
                    neighbor_node = neighbor_node.copy_replace_cost(new_cost)
                    heappush(queue, neighbor_node)

    return visited


def get_reachable(network, val, has_keys):
    reachable = []
    for other_val in network[val]:
        if other_val.islower() or other_val == "@":
            reachable.append(other_val)
        elif other_val.lower() in has_keys:
            reachable.append(other_val)
    return reachable


if __name__ == '__main__':
    _world_map = """
#################################################################################
#.......#.......#.......O...#.D.........#.......#.......#.....U...#...#.......#.#
#.#####.#.#######.#####.#.###.#########.#####.#.#.###.###.#.###.###.#.#.###.#.#.#
#...#.#.#............j#.#.#...#.....#b..#.....#.#.#.#.#...#.#...#...#...#...#...#
#.#.#.#.#.###########.#.#.#.###.#.###.###.#######.#.#.#.###.#####.#######.#####.#
#v#.#.#.#.#.#...#.....#.#.#.#...#.#...#.#...#.....#.#...#.#...#...#.......#.....#
#.#.#.#.#.#.#.#.#######.#.#.#.#####.###.#.#.#.#####.#####.###.#.###.###########.#
#.#.#r#.#...#.#...#.....#.#.#.#.....#...#.#...#.......#.....#.....#.....A.....#.#
###.#.#.###.#.###.#.#####.#.#.#.#######.#.#####.#####.#.#########.#########.#.#.#
#...#...#...#.#.....#.....#...#.#.....#.#.#.....#.....#...#...#.....#.....#.#.#.#
#.###.###.###.#.#######.###.###.###.#.#.#.#.#####.#######.#.#.#######.###.###.###
#.#.....#.#...#.#.....#.#...#...#...#.N.#.#.#...#.......#.#.#...#...#s..#...#...#
#.#####.###.#####.###.###.###.###.#######.#.#.#.#######.#.#C###.#.#.###.###.###.#
#...#.......#.....#.#.......#.#...#.....#.#...#.#.#.....#.#...#..c#...#.#...X.#.#
#.#.#.#######.#####.#########.#.###.###.#.#####.#.#.#####.###.#######Y#.#####.#.#
#.#.#.#...#...#.....#.........#.......#.#.......#...#.......#g......#.#.....#...#
#.#.###.#.#.#######.#.#########.#######.#########.###.#.###########.#.#####.###.#
#.#.....#.#.......#.#.#.......#...#.....#.#.......#...#...........#.#.......#...#
#######.#.#######.#.#.###.###.#####.###.#.#.#######.#############.#.#########.###
#.....#.#.......#...#...#...#...#...#...#.#.....#...#.....#.......#...#.....#.#.#
#.###.###.#####.###.###.#.#.###.#.###.###.#####.#.#######.#Q#######.#.###.###.#.#
#.#...#...#...#.#...#...#.#...#...#.#...#.#.....#.........#.#...P.#.#.G.#.....#.#
#.###.#.###.###.#.#########.#.#####.###.#.#.###############.#####.#.###.#.#####.#
#...#...#...#...#.........#.#.#.....#...#.#.#.......#.........#...#...#.#.....#.#
###.#####.###.###########.###.###.###.###.#.#.###.#.#.#####.###.#####.#.#####.#.#
#...#...#...#.#.......#.#...#...#.......#...#...#.#.#...#...#...#.....#i..#.#...#
#.###.###.#.#.#####.#.#.###.###.#######.#.#######.#.###.#.###.#########.#.#.###.#
#.#...#...#.#...#...#.....#...#.....#...#.#.......#.....#.#p..#.......#.#.#.#...#
#.#.#.#.###.###.#.#.#####.###.#####.#####.###.#########.###.###.#####.###.#.#.###
#.#.#...#.#...#.#.#.#...#...#.....#.....#...#.#...#.....#...#...#.#..l#...#.....#
#.###.###.###.#.#.###.#.###.#####.#####.###.#.#.#.#######.###L###.#.###.#########
#...#.#.....#...#.....#.#.#...#..e#.....#...#...#.....#.Z.#...#..t#.T.#......w..#
###.#.#.###.###########.#.###.#.###.#####.###.#######.#.###.###.#.###.#.#######.#
#...#.#.#.#.........#...#...#.#.#....h..#.#...#.......#.#...#.F.#...#.#.I.....#.#
#.###.#.#.#.#######.#.###.###.#.#.#####.#.#####.#####.#.#.###.#####.#.#.#######.#
#.#.....#...#.....#.#.#.......#.#.#...#.#.......#.#...#..z#.#.....#...#.#..k..#.#
#.#########.#.###.#.#.#########.#.#.#.#.#########.#.#######.#####.#######.###.#.#
#...M.#...#.#.#.#.#...#.....#...#.#.#...#...#.....#.#.........#...#.......#.#.#.#
#.###.#.#.###.#.#.#####.###.#.#####.###.#.#.#.#.###.###.#####.#.###.#######.#W#.#
#...#...#.......#.........#.........#.....#...#.........#.....#fK...#...........#
#######################################.@.#######################################
#.......#.........#...................#.......#.........#...........#...........#
#.###.###.#.#######.#####.#.#########.#.#.###.#.#####.#.#.#########.#.#######.#.#
#.#...#...#.........#...#.#.#.......#...#...#.#.#...#.#.#.#.#.....#.#.......#.#.#
#.#.###.#############.#.###.#.#####.###.###.###.#.#.#.###.#.#.#.###.#####.###.#.#
#.#...#.#.........#...#...#.#.....#...#.#...#...#.#.#.....#...#...#...#...#...#.#
#.#####.#########.#.#####.#.#####.#.###.#.#.#.#####.#############.###.#.###.###.#
#.......#...#...#.#.....#.#...#...#.#...#.#.#...#.........#.....#.#...#...#...#.#
#.#######.#.#.#.#.#####.#.#.#.#.###.#.###.#.###.#.#######.#.###.#.#.#####.###.###
#...#.....#...#.....#...#.#.#.#.#...#...#.#.#.#.#...#.....#...#...#.#.......#...#
###.#.#.#########.###.###.###.#.#.#####.#.#.#.#.###.#####.###.#####.#.#########.#
#.#.#.#.#.....#...#...#.#.....#.#...#...#.#...#...#..m..#...#.....#.#.....#...#.#
#.#.###.#.###.#####.###.#######.#####.###.#######.#####.###.#####.#.#.#####.#.#.#
#.#..q..#.#.#.#.....#...............#...#.......#.....#...#.#.....#.#.#...#.#...#
#.#.#####.#.#.#.###.#######.#######.###.#.#####.#####.#.#.#.#.###.#.#.#.#.#.###.#
#...#.....#.....#...#.....#.#.....#.....#...#.#.H.#...#.#.#...#...#.#.#.#...#.#.#
#.###.#.#########.###.###.###.###.#########.#.###.#.#####.#####.###.#.#.#####.#.#
#.#.#.#.#...#...#...#.#.......#.#.#.....#.#.#...#.........#.....#...#.#.#.....#.#
#.#.#.###.#.#.#.###.#.#########.#.#.###.#.#.#.###################.###.#.###.#.#.#
#...#.....#...#.#.#.#...#.......#...#.#.#.#.#.......#.....#.....#.#...#...#.#.#.#
###.###########.#.#.###.#.#####.#####.#.#.#.#######.#.###.#.###.#.#######.###.#.#
#...#.........#.#...#...#.#...#.......#.#...#.....#.#.#.#...#...#.....#...#...#.#
#.###.#######.#.###########.#.#.#.###.#.#.###.###.#.#.#.#############.#.###.#.#.#
#.#...#.#.......#.........#.#.#.#.#...#.#.#.....#...#...#.........#...#...#.#.#.#
#.#.###.#.#####.#.###.###.#.#.###.#####.#.#####.#######.#.###.###.#.###.#.#.###.#
#.#.#.#...#...#.#.#.#.#.....#...#.#.....#.......#.......#...#.#...#...#.#.#.....#
###.#.#.###.#.###.#.#.#########.#.#.###########.#.###########.#.#####.#.#.#####.#
#...#...#...#.....#.#.........#...#.#...#.....#.#.....#.......#.#.....#.#.....#.#
#.###.###.#########.#########.#####.###.#####.#.#####.###.#####.#.#####.#####R#J#
#.#.#...#.#.......#.....#...#o......#...#.....#.E...#.....#...#...#.....#.#...#.#
#.#.#.###.#.###.#.#.###.###.#########.###.#########.#########.#########.#.#.#####
#.#...#...#...#.#.#...#...........#.....#.#.......#...#.....#.........#.#.#.....#
#.#####.#####.#.#.#.#.###########.#.###.#.#.#.#.#####.#.###.#.#.#####.#.#.#####.#
#.#.....#.....#.#.#.#.#......a....#...#.#...#.#.#...#.#...#.#.#...#...#.....#...#
#.#.###########.#.###.#.###############.#.###.#.#.#.#.###.#.#####.###.#######.#.#
#...#u......#...#.....#...#.......#...#.#...#.#.#.#.#.#...#.#...#...#.B...#...#.#
#.#######.#.#.###########.#.#####.#.#.#.###.#.###.#.#.#.###.#.#.###.#####.#.###.#
#.#.....#.#.#...#...#...#x#...#.#.#.#...#.#.#.....#.#.#.#.#.#.#...#..d#...#.V.#.#
#.###.#.#.#.###.#.#.#.#.#.###.#.#.#S###.#.#.#######.#.#.#.#.#.###.###.#.#####.#.#
#.....#...#.....#.#...#.......#.....#..y#.........#.....#n....#.......#.......#.#
#################################################################################
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

    n_keys = len(_keys)

    state = State('@', network)
    shortest_path(state, len(_keys))
    print(best_state.has_keys)
    print(best_state.cost)


