import re
from src.helpers import clean_lines_iter, read
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
        if val.islower() or val.isnumeric():
            paths[val] = (dist, obstacles)
        elif val.isupper():
            obstacles = (*obstacles, val.lower())

        for other_pos in passages[pos]:
            if other_pos in visited:
                continue
            queue.append((other_pos, dist + 1, obstacles))

    start_val = _get(world_map, start)
    paths.pop(start_val)
    return {start_val: paths}


def _get(arr, pos):
    i, j = pos
    return arr[i][j]


INF = 1e9


def get_final_shortest_path(all_shortest_paths, common_paths, key_to_robot, start_val, n_keys):

    visited = set()
    min_dist = defaultdict(lambda: INF)
    queue = [(0, start_val, frozenset(), common_paths)]

    while queue:
        dist, val, state, _common_paths = heappop(queue)
        key = (val, state)

        if key not in visited:
            visited.add(key)

            if len(state) == n_keys:
                continue

            state = _add_to_state_if_key(state, val)
            for other_val, (_dist, obstacles) in {**all_shortest_paths[val], **_common_paths}.items():
                if not _can_move_past_obstacles(state, obstacles):
                    continue

                other_state = _add_to_state_if_key(state, other_val)
                other_key = (other_val, other_state)

                new_cost = dist + _dist
                if new_cost < min_dist[other_key]:
                    min_dist[other_key] = new_cost
                    other_common_paths = _replace_in_common_paths(other_val, _common_paths, key_to_robot)
                    heappush(queue, (new_cost, other_val, other_state, other_common_paths))

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


def _replace_in_common_paths(key, common_paths, key_to_robot):
    robot = key if key.isnumeric() else key_to_robot[key]
    for old_key in common_paths:
        if old_key == robot or (old_key.isalpha() and key_to_robot[old_key] == robot):
            break
    common_paths = dict(common_paths)
    common_paths.pop(old_key)
    common_paths[key] = (0, ())
    return common_paths


if __name__ == '__main__':
    world_map = read("keys2.txt")

    i = 0
    while '@' in world_map:
        world_map = world_map.replace('@', str(i), 1)
        i += 1

    world_map = list(clean_lines_iter(world_map))
    _robots = list(find_x(world_map, r"\d"))
    _keys = find_x(world_map, "[a-z]")
    _doors = find_x(world_map, "[A-Z]")
    _passage = find_x(world_map, r"[a-zA-Z\d.]")
    _passage = parse_passage(_passage)

    all_shortest_paths = {}
    for x in _robots + list(_keys):
        all_shortest_paths.update(shortest_path(x, _passage, world_map))

    # Find out which robot each key "belongs to"
    key_to_robot = {}
    common_paths = {}
    for r in _robots:
        rnum = _get(world_map, r)
        for k in all_shortest_paths[rnum]:
            assert k not in key_to_robot
            key_to_robot[k] = rnum

        common_paths[rnum] = (0, ())

    lowest = get_final_shortest_path(all_shortest_paths, common_paths, key_to_robot, '0', len(_keys))
    print(lowest)
