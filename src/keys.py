import re
from src.helpers import clean_lines_iter
from heapq import heappush, heappop
from collections import defaultdict


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
            queue.append((other_pos, dist + 1, obstacles))

    start_val = _get(world_map, start)
    paths.pop(start_val)
    return start_val, paths


def _get(arr, pos):
    i, j = pos
    return arr[i][j]


INF = 1e9


def get_final_shortest_path(all_shortest_paths, start_val, n_keys):
    visited = set()
    min_dist = defaultdict(lambda: INF)
    queue = [(0, start_val, frozenset())]

    while queue:
        dist, val, state, = heappop(queue)
        key = (val, state)
        print(key, dist)

        if key not in visited:
            visited.add(key)

            if len(state) == n_keys:
                continue

            state = _add_to_state_if_key(state, val)
            for other_val, (_dist, obstacles) in all_shortest_paths[val].items():
                if not _can_move_past_obstacles(state, obstacles):
                    continue

                other_state = _add_to_state_if_key(state, other_val)
                other_key = (other_val, other_state)

                new_cost = dist + _dist
                if new_cost < min_dist[other_key]:
                    min_dist[other_key] = new_cost
                    heappush(queue, (new_cost, other_val, other_state))

    return lowest_dist(min_dist)


def lowest_dist(min_dist_per_node):
    best = INF
    for (val, state), cost in min_dist_per_node.items():
        if len(state) < len(_keys):
            continue
        if cost < best:
            best = cost
    return best


def _add_to_state_if_key(state, val):
    if val.islower():
        state = frozenset([*state, val])
    return state


def _can_move_past_obstacles(state, obstacles):
    return all(key in state for key in obstacles)


if __name__ == '__main__':
    world_map = """
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#.b#
#######
    """
    world_map = list(clean_lines_iter(world_map))
    _robots = list(find_x(world_map, "@"))
    _keys = find_x(world_map, "[a-z]")
    _doors = find_x(world_map, "[A-Z]")
    _passage = find_x(world_map, "[a-zA-Z@.]")
    _passage = parse_passage(_passage)

    sp = defaultdict(dict)
    for r in _robots:
        key, paths = shortest_path(r, _passage, world_map)
        sp[key].update(paths)
    for k in _keys:
        key, paths = shortest_path(k, _passage, world_map)
        sp[key].update(paths)

    for k, v in sp.items():
        print(k, v)

    lowest = get_final_shortest_path(sp, '@', len(_keys))
    print(lowest)
