from src.helpers import read
import re
from collections import defaultdict


def build_map(map_lines):
    tiles_and_portals = _find_pattern_in_map(map_lines, r"[\.A-Z]")
    portals = _find_portals(map_lines, tiles_and_portals)
    passage = _find_passage(map_lines, tiles_and_portals)

    start = portals.pop("AA")[0]
    end = portals.pop("ZZ")[0]

    for pos1, pos2 in portals.values():
        passage[pos1].add(pos2)
        passage[pos2].add(pos1)

    return start, end, passage


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


def shortest_path(start, end, passage):
    visited = set()
    queue = [(start, 0)]

    while queue:
        pos, dist = queue.pop(0)
        visited.add(pos)
        if pos == end:
            return dist
        for other_pos in passage[pos]:
            if other_pos in visited:
                continue
            queue.append((other_pos, dist+1))

    return None


if __name__ == '__main__':
    with open("../input/maze.txt") as f:
        maze_str = "".join(filter(lambda x: x.strip(), f))

    maze_str_lines = maze_str.splitlines()
    # start, end, passage = build_map(maze_str_lines)
    # print(shortest_path(start, end, passage))

