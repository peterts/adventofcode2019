from src.helpers import read, read_comma_separated_list, read_line_separated_list
from src.int_program import IntProgram, STATE_HALTED, STATE_RUNNING
from collections import defaultdict, Counter


def initialize_board(memory):
    program = IntProgram(memory)
    program.run()

    i = 0
    tiles = defaultdict(int)

    while i < len(program.output):
        x, y, tile = program.output[i:i+3]
        tiles[(x, y)] = tile
        i += 3

    return tiles, program


def find_first(tiles, value):
    for position, _value in tiles.items():
        if value == _value:
            return position
    return None


def play_game_using_ai(tiles, program):
    ball = find_first(tiles, 4)
    paddle = find_first(tiles, 3)

    program.restart()
    program.memory[0] = 2

    def get_move():
        if ball[0] < paddle[0]:
            return -1
        if ball[0] > paddle[0]:
            return 1
        return 0

    while program.state != STATE_HALTED:
        move = get_move()
        program.run([move])
        i = 0
        while i < len(program.output):
            x, y, score = program.output[i:i+3]
            i += 3

        paddle = (paddle[0] + move, paddle[1])
        ball = (x, y)

    return score


if __name__ == '__main__':
    memory = read_comma_separated_list("game.txt", int)
    tiles, program = initialize_board(memory)
    counter = Counter(tiles.values())
    print(counter[2])
    print(play_game_using_ai(tiles, program))
