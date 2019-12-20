from src.helpers import read
import re
from collections import defaultdict


def build_map(map_lines):
    tiles_and_portals = _find_pattern_in_map(map_lines, r"[\.A-Z]")
    portals = _find_portals(map_lines, tiles_and_portals)
    passage = _find_passage(map_lines, tiles_and_portals)

    port_vals = [p for positions in portals.values() for p in positions]
    min_y, max_y = min(port_vals, key=lambda p: p[0])[0], max(port_vals, key=lambda p: p[0])[0]
    min_x, max_x = min(port_vals, key=lambda p: p[1])[1], max(port_vals, key=lambda p: p[1])[1]

    start = portals.pop("AA")[0]
    end = portals.pop("ZZ")[0]

    def _is_inside(_pos):
        y, x = _pos
        return min_x < x < max_x and min_y < y < max_y

    negative_transports = []
    positive_transports = []

    for pos1, pos2 in portals.values():
        if _is_inside(pos1):
            positive_transports.append((pos1, pos2))
            negative_transports.append((pos2, pos1))
        else:
            positive_transports.append((pos2, pos1))
            negative_transports.append((pos1, pos2))

        passage[pos1].add(pos2)
        passage[pos2].add(pos1)

    return start, end, passage, negative_transports, positive_transports


def _find_portals(map_lines, tiles_and_portals):
    portals = defaultdict(list)

    for pos in tiles_and_portals:
        if not _is_portal(map_lines, pos):
            continue
        for direction in ["R", "D"]:
            neighb_pos = move_one_step_in_direction[direction](*pos)
            if _is_portal(map_lines, neighb_pos):
                portal_key = _get(map_lines, pos) + _get(map_lines, neighb_pos)
                portal_to = _find_open_pos_for_portal(map_lines, pos, neighb_pos)
                portals[portal_key].append(portal_to)

    return portals


def _find_passage(map_lines, tiles_and_portals):
    tiles = list(filter(lambda _pos: _is_open(map_lines, _pos), tiles_and_portals))

    passage = defaultdict(set)

    for pos in tiles:
        for other_pos in tiles:
            if _is_connected(pos, other_pos):
                passage[pos].add(other_pos)

    return passage


def _find_open_pos_for_portal(map_lines, *portal_positions):
    for pos in portal_positions:
        for direction in move_one_step_in_direction:
            neighb_pos = move_one_step_in_direction[direction](*pos)
            if _is_open(map_lines, neighb_pos):
                return neighb_pos
    return None


def _is_connected(pos, other_pos):
    return ((pos[0] == other_pos[0]) and abs(pos[1] - other_pos[1]) == 1) or \
           ((pos[1] == other_pos[1]) and abs(pos[0] - other_pos[0]) == 1)


move_one_step_in_direction = {
    "R": lambda i, j: (i, j+1),
    "L": lambda i, j: (i, j-1),
    "U": lambda i, j: (i-1, j),
    "D": lambda i, j: (i+1, j)
}

opposite_direction = {"R": "L", "L": "R", "U": "D", "D": "U"}


def _find_pattern_in_map(map_lines, x, return_first=False):
    found = []

    for i, line in enumerate(map_lines):
        for match in re.finditer(x, line):
            found.append((i, match.start()))
            if return_first:
                return found

    return set(found)


def _get(arr, pos, default=""):
    try:
        i, j = pos
        return arr[i][j]
    except IndexError:
        return default


def _is_open(map_lines, pos):
    return _get(map_lines, pos) == "."


def _is_portal(map_lines, pos):
    return _get(map_lines, pos).isupper()


def shortest_path(start, end, passage, negative=(), positive=()):
    visited = set()
    queue = [(start, 0, 0)]

    while queue:
        pos, dist, state = queue.pop(0)
        visited.add((pos, state))

        if (pos, state) == (end, 0):
            return dist

        for other_pos in passage[pos]:
            other_state = state
            if (pos, other_pos) in negative:
                other_state -= 1
            elif (pos, other_pos) in positive:
                other_state += 1
            if other_state < 0:
                continue

            if (other_pos, other_state) in visited:
                continue

            queue.append((other_pos, dist+1, other_state))

    return None


if __name__ == '__main__':
    with open("../input/maze.txt") as f:
        maze_str = "".join(filter(lambda x: x.strip(), f))

    maze_str_lines = maze_str.splitlines()
    start, end, passage, negative_transports, positive_transports = build_map(maze_str_lines)
    print(shortest_path(start, end, passage))
    print(shortest_path(start, end, passage, negative_transports, positive_transports))




