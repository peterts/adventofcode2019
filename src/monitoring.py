from dataclasses import dataclass

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

    m = []
    for row in inp.splitlines():
        if row.strip():
            m.append(list(map(lambda c: c == "#", row.strip())))

    asteroids = []

    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j]:
                asteroids.append((i, j))

    n_visible = [[0]*len(m[0]) for _ in range(len(m))]

    checked = set()

    for i, ast in enumerate(asteroids):
        x, y = ast
        for j, ast2 in enumerate(asteroids):
            x2, y2 = ast2
            if i == j:
                continue
            if (i, j) in checked:
                continue
            for k, other_ast in enumerate(asteroids):
                if k == i or k == j:
                    continue
                if is_between(Point(*ast), Point(*ast2), Point(*other_ast)):
                    break
            else:
                n_visible[x][y] += 1
                n_visible[x2][y2] += 1
                checked.add((i, j))
                checked.add((j, i))

    print(max(i for row in n_visible for i in row))

    m = None
    count = -1

    for i, row in enumerate(n_visible):
        for j, x in enumerate(row):
            if x > count:
                m = (i, j)
                count = x

    print(count)
    print(m)
    print(max(i for row in n_visible for i in row))




