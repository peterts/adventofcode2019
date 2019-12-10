from dataclasses import dataclass
from heapq import heappush
from math import sqrt, atan2, pi
from cmath import phase


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


def angle(v1, v2):
    ang = phase(complex(*v1)) - phase(complex(*v2))
    if ang < 0:
        return 2*pi + ang
    return ang


def get_all_visible_from_ast_ordered_by_degree(ast, ast_map):
    asteroids = []

    for i in range(len(ast_map)):
        for j in range(len(ast_map[0])):
            if ast_map[i][j]:
                asteroids.append((i, j))

    visible_from_ast = []
    degs = []

    for ast2 in asteroids:
        if ast == ast2:
            continue
        for ast3 in asteroids:
            if ast == ast3 or ast2 == ast3:
                continue
            if is_between(Point(*ast), Point(*ast2), Point(*ast3)):
                break
        else:
            v = ast2[1] - ast[1], ast[0] - ast2[0]
            d = angle((0, 1), v)
            visible_from_ast.append(ast2)
            degs.append(d)

    if not visible_from_ast:
        return []
    ix = sorted(range(len(visible_from_ast)), key=lambda i: degs[i])
    print([degs[i] for i in ix])
    print(len(set(degs)) == len(list(degs)))
    return [visible_from_ast[i] for i in ix]


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

    ast_map = []
    for row in inp.splitlines():
        if row.strip():
            ast_map.append(list(map(lambda c: c == "#", row.strip())))

    asteroids = []

    for i in range(len(ast_map)):
        for j in range(len(ast_map[0])):
            if ast_map[i][j]:
                asteroids.append((i, j))

    ast = (28, 26)
    destroyed = []
    visible = get_all_visible_from_ast_ordered_by_degree(ast, ast_map)
    print(len(visible))
    while visible:
        for other_ast in visible:
            destroyed.append(other_ast)
            x, y = other_ast
            ast_map[x][y] = False
        visible = get_all_visible_from_ast_ordered_by_degree(ast, ast_map)

    print(destroyed[0:3])
    print(destroyed[9])
    print(destroyed[19])
    print(destroyed[49])
    print(destroyed[199])
    print(destroyed[190:210])
    print((2, 8) in destroyed)

    print(destroyed[199][1] * 100 + destroyed[199][0])



