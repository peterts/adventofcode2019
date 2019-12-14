from src.game import play_game_using_ai, initialize_board
from src.helpers import read_comma_separated_list
from collections import Counter


def test_game():
    memory = read_comma_separated_list("game.txt", int)
    tiles, program = initialize_board(memory)
    counter = Counter(tiles.values())
    assert counter[2] == 298
    assert play_game_using_ai(tiles, program) == 13956
