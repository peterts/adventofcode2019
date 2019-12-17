import math
from functools import lru_cache
from itertools import accumulate


def compute_phase(values, base_pattern, n_repeats=1):
    values_out = []
    num_values_in_one_repetition = len(values) // n_repeats

    for i in range(len(values)):
        print(i)
        cycle_time = get_cycle_time(base_pattern, num_values_in_one_repetition, i)
        gen = yield_pattern(base_pattern, i+1)

        cumsums = [0]
        s = 0
        for j in range(min(n_repeats+1, cycle_time+1)):
            s += sum(x*p for x, p in zip(values, next_n(gen, num_values_in_one_repetition)))
            cumsums.append(s)

        x = n_repeats // (cycle_time + 1)
        value = x * cumsums[-1]
        value += cumsums[n_repeats - (x * (cycle_time + 1))]

        values_out.append(last_digit(value))

    return values_out


def yield_pattern(base_pattern, n_repeats):
    skip = True
    while 1:
        for i in base_pattern:
            for _ in range(n_repeats):
                if skip:
                    skip = False
                    continue
                yield i


def next_n(gen, n):
    for _ in range(n):
        yield next(gen)


def last_digit(num):
    return int(str(num)[-1])


def rev_accumulate(arr):
    s = sum(arr)
    for x in arr:
        yield s
        s -= x


if __name__ == '__main__':
    values_str = "03036732577212944063491565474664" * 10000
    message_offset = int(values_str[:7])

    values = list(map(int, values_str))

    base_pattern = (0, 1, 0, -1)

    values = values[message_offset:]
    for _ in range(100):
        values = list(map(last_digit, rev_accumulate(values)))

    print(''.join(map(str, list(values)[:8])))
