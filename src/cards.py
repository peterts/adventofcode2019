from functools import partial
from src.helpers import read_line_separated_list


def deal_new_stack(cards):
    return cards[::-1]


def cut_n_cards(n, cards):
    return cards[n:] + cards[:n]


def deal(n, cards):
    m = len(cards)
    new_cards = [None] * m
    leftmost = 0
    for i in range(m):
        j = (i*n + leftmost) % m
        if new_cards[j] is not None:
            leftmost += 1
            j += 1
        new_cards[j] = cards[i]
    return new_cards


commands = (
    ("deal into new stack", deal_new_stack),
    ("deal with increment", deal),
    ("cut", cut_n_cards)
)


def parse_line(line):
    for command, func in commands:
        if line[:len(command)] == command:
            if len(line) > len(command):
                n = int(line[len(command):])
                return partial(func, n)
            return func


if __name__ == '__main__':
    cards = list(range(119315717514047))

    for line in read_line_separated_list("cards.txt"):
        func = parse_line(line)
        cards = func(cards)

    print(cards.index(2019))

