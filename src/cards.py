"""
Only day I had to cheat. Thanks for the explanation mcpower_
(https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/)
"""
from dataclasses import dataclass
from src.helpers import modinv, read_line_separated_list


@dataclass
class Deck:
    size: int
    first_card: int = 0
    increment: int = 1
    card_num: int = 0

    def new_stack(self):
        self.increment *= -1
        self.first_card += self.increment

    def cut(self, n):
        self.first_card += self.increment * n

    def deal(self, n):
        self.increment *= modinv(n, self.size)

    def get_card(self, card_num):
        return (card_num * self.increment + self.first_card) % self.size

    def __iter__(self):
        self.card_num = 0
        return self

    def __next__(self):
        if self.card_num < self.size:
            return_val = self.get_card(self.card_num)
            self.card_num += 1
            return return_val
        raise StopIteration

    def exec(self, command_str):
        commands = (
            ("deal into new stack", self.new_stack),
            ("deal with increment", self.deal),
            ("cut", self.cut)
        )

        for command_key, command_func in commands:
            if command_str.startswith(command_key):
                if len(command_str) > len(command_key):
                    command_func(int(command_str[len(command_key):]))
                else:
                    command_func()

    def exec_all(self, commands_iter):
        for command_str in commands_iter:
            self.exec(command_str)

    def exec_all_n_times(self, commands_iter, n):
        self.exec_all(commands_iter)

        increment_multiplier_per_pass = self.increment
        first_card_after_initial_pass = self.first_card

        self.increment = pow(increment_multiplier_per_pass, n, self.size)
        self.first_card = first_card_after_initial_pass * (1 - self.increment) * modinv(1 - increment_multiplier_per_pass, self.size)


if __name__ == '__main__':
    deck = Deck(10007)
    commands_iter = read_line_separated_list("cards.txt")
    deck.exec_all(commands_iter)

    cards = list(deck)
    print(cards.index(2019))

    deck2 = Deck(119315717514047)
    n_passes = 101741582076661
    deck2.exec_all_n_times(commands_iter, n_passes)
    print(deck2.get_card(2020))





