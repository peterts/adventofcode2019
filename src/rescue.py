from src.helpers import read_comma_separated_list, clean_lines_iter
from src.int_program import IntProgram
import networkx as nx
import dwave_networkx as dnx
import dimod


def is_intersection(lines, i, j, n, m):
    if i < 1 or i > n - 2 or j < 1 or j > m - 2:
        return False
    return all(lines[k][l] == "#" for k, l in ((i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)))


new_direction = {
    ("U", 0): "L", ("U", 1) : "R",
    ("D", 0): "R", ("D", 1): "L",
    ("R", 0): "U", ("R", 1): "D",
    ("L", 0): "D", ("L", 1): "U",
}

move_one_step_in_direction = {
    "R": lambda i, j: (i, j+1),
    "L": lambda i, j: (i, j-1),
    "U": lambda i, j: (i-1, j),
    "D": lambda i, j: (i+1, j)
}

TURN_RIGHT = {"U": "R", "R": "D", "D": "L", "L": "U"}
TURN_LEFT = dict((v, k) for k, v in TURN_RIGHT.items())


def can_move(lines, i, j, direction):
    k, l = move_one_step_in_direction[direction](i, j)
    return -1 < k < n and -1 < l < m and lines[k][l] == "#"


if __name__ == '__main__':
    memory = read_comma_separated_list("rescue.txt", int)
    program = IntProgram(memory)
    program.run()
    s = ''.join(map(chr, program.output))

    lines = list(clean_lines_iter(s))
    n = len(lines)
    m = None

    intersections = []
    # graph = nx.Graph()

    robot_or_scaffold = "#>^v<"

    robot = None
    n_scaffolds = 0

    for i, line in enumerate(lines):
        if m is None:
            m = len(line)
        for j, c in enumerate(line):
            if lines[i][j] in robot_or_scaffold:
                n_scaffolds += 1
                if robot_or_scaffold.index(lines[i][j]) > 0:
                    robot = (i, j)
                # for k, l in (i-1, j), (i+1, j), (i, j-1), (i, j+1):
                #     if k < 0 or l < 0:
                #         continue
                #     try:
                #         if lines[k][l] in robot_or_scaffold:
                #             graph.add_edge((i, j), (k, l))
                #     except IndexError:
                #         continue

            if is_intersection(lines, i, j, n, m):
                intersections.append(i*j)

    print(n_scaffolds)
    print(s)

    i, j = robot
    direction = "UDLR"["^v<>".index(lines[i][j])]
    n_visited = 1

    operations = []

    steps = 0
    while n_visited < n_scaffolds:
        if can_move(lines, i, j, direction):
            steps += 1
        else:
            if steps > 0:
                operations.append(steps)
            steps = 0

            if can_move(lines, i, j, TURN_RIGHT[direction]):
                direction = TURN_RIGHT[direction]
                operations.append("R")
            elif can_move(lines, i, j, TURN_LEFT[direction]):
                direction = TURN_LEFT[direction]
                operations.append("L")
            else:
                direction = TURN_RIGHT[TURN_RIGHT[direction]]
                operations.append("R")
                operations.append("R")

        i, j = move_one_step_in_direction[direction](i, j)

        n_visited += 1

    print(operations)

    # graph = graph.to_undirected()
    #
    # paths = dict(nx.all_pairs_shortest_path(graph))
    #
    # graph2 = nx.Graph()
    # edges = []
    #
    # for node in graph.nodes:
    #     for other_node in graph.nodes:
    #         if other_node == node:
    #             continue
    #         edges.append([node, other_node, len(paths[node][other_node])])
    #
    # graph2.add_weighted_edges_from(edges)
    # print(dnx.traveling_salesperson(graph2, dimod.ExactSolver(), start=robot))


