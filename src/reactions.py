import re
from src.helpers import read, clean_lines_iter
from collections import defaultdict
from math import ceil


MATERIAL_PATTERN = r"(?P<q>\d+) (?P<n>[A-Z]+)"


def parse_reactions(reactions_str):
    reactions = {}
    for row in clean_lines_iter(reactions_str):
        inp = []
        inp_str, out_str = row.split("=>", maxsplit=1)
        for match in re.finditer(MATERIAL_PATTERN, inp_str):
            inp.append((match.group("n"), int(match.group("q"))))
        match = re.search(MATERIAL_PATTERN, out_str)
        out_n, out_q = match.group("n"), int(match.group("q"))
        reactions[out_n] = (out_q, inp)
    return reactions


class MaterialFactory:
    def __init__(self, reactions):
        self.reactions = reactions
        self.produced = defaultdict(int)
        self.required = defaultdict(int)
        self.cost = 0

    def produce(self, material, amount):
        if material not in reactions:  # Ore
            self.cost += amount
            return

        produced_by_one_reaction, reaction = self.reactions[material]
        self.required[material] += amount
        n_to_produce = ceil((self.required[material] - self.produced[material]) / produced_by_one_reaction)
        if n_to_produce > 0:
            for child_material, child_amount in reaction:
                self.produce(child_material, n_to_produce * child_amount)

        self.produced[material] += n_to_produce * produced_by_one_reaction


if __name__ == '__main__':
    reactions = parse_reactions(read("reactions1.txt"))
    factory = MaterialFactory(reactions)

    factory.produce("FUEL", 1)
    print(factory.cost)

    n = 1
    budget = 1000000000000
    while factory.cost < budget:
        n += 1
        factory.produce("FUEL", 1)
        print(f"\r{factory.cost / budget}", end="")

    print()
    if factory.cost == budget:
        print(n)
    else:
        print(n-1)
