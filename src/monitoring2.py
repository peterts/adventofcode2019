from dataclasses import dataclass
from sortedcontainers import SortedList
from heapq import heappush
from math import sqrt, atan2, pi


@dataclass
class Point:
    x: int
    y: int


def is_between(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > 1e-9:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True


def dist(a, b):
    return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


def deg(a, b):
    dot = a.x * b.x + a.y * b.y  # dot product
    det = a.x * b.y - a.y * b.x  # determinant
    print(atan2(det, dot))  # atan2(y, x) or atan2(sin, cos)
    return atan2(det, dot)


def angle(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    dot = x1 * x2 + y1 * y2  # dot product
    det = x1 * y2 - y1 * x2  # determinant
    angle = atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    if angle < 0:
        return angle % (2*pi)
    if x2 < 0:
        return 2*pi - angle
    return angle


def get_all_visible_from_ast_ordered_by_degree(ast, ast_map):
    asteroids = []

    for i in range(len(ast_map)):
        for j in range(len(ast_map[0])):
            if ast_map[i][j]:
                asteroids.append((i, j))

    visible_from_ast = []
    for ast2 in asteroids:
        if ast == ast2:
            continue
        for ast3 in asteroids:
            if ast == ast3 or ast2 == ast3:
                continue
            if is_between(Point(*ast), Point(*ast2), Point(*ast3)):
                break
        else:
            v = ast2[1] - ast[1], ast2[0] - ast[0]
            d = angle((0, 1), v)
            print(d)
            heappush(visible_from_ast, (d, ast2))

    if not visible_from_ast:
        return []
    _, visible_from_ast_list = zip(*visible_from_ast)
    return visible_from_ast_list


if __name__ == '__main__':
    inp = """
#....#.....#...#.#.....#.#..#....#
#..#..##...#......#.....#..###.#.#
#......#.#.#.....##....#.#.....#..
..#.#...#.......#.##..#...........
.##..#...##......##.#.#...........
.....#.#..##...#..##.....#...#.##.
....#.##.##.#....###.#........####
..#....#..####........##.........#
..#...#......#.#..#..#.#.##......#
.............#.#....##.......#...#
.#.#..##.#.#.#.#.......#.....#....
.....##.###..#.....#.#..###.....##
.....#...#.#.#......#.#....##.....
##.#.....#...#....#...#..#....#.#.
..#.............###.#.##....#.#...
..##.#.........#.##.####.........#
##.#...###....#..#...###..##..#..#
.........#.#.....#........#.......
#.......#..#.#.#..##.....#.#.....#
..#....#....#.#.##......#..#.###..
......##.##.##...#...##.#...###...
.#.....#...#........#....#.###....
.#.#.#..#............#..........#.
..##.....#....#....##..#.#.......#
..##.....#.#......................
.#..#...#....#.#.....#.........#..
........#.............#.#.........
#...#.#......#.##....#...#.#.#...#
.#.....#.#.....#.....#.#.##......#
..##....#.....#.....#....#.##..#..
#..###.#.#....#......#...#........
..#......#..#....##...#.#.#...#..#
.#.##.#.#.....#..#..#........##...
....#...##.##.##......#..#..##....
    """

    inp = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
    """

    ast_map = []
    for row in inp.splitlines():
        if row.strip():
            ast_map.append(list(map(lambda c: c == "#", row.strip())))

    asteroids = []

    for i in range(len(ast_map)):
        for j in range(len(ast_map[0])):
            if ast_map[i][j]:
                asteroids.append((i, j))

    ast = (13, 11)
    destroyed = []
    visible = get_all_visible_from_ast_ordered_by_degree(ast, ast_map)
    while visible:
        print(len(visible))
        for other_ast in visible:
            destroyed.append(other_ast)
            x, y = other_ast
            ast_map[x][y] = False
        visible = get_all_visible_from_ast_ordered_by_degree(ast, ast_map)

    print(destroyed[0:10])
    print(destroyed[200])
    print(destroyed[190:210])
    print((2, 8) in destroyed)

    print(destroyed[200][0] * 100 + destroyed[200][1])




