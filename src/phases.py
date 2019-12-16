import math


def compute_phase(values, base_pattern_matrix):
    values_out = []
    for i in range(len(values)):
        values_out.append(
            int(str(sum(x*p for x, p in zip(values, base_pattern_matrix[i])))[-1])
        )
    return values_out


def create_base_pattern_matrix(base_pattern, n_digits):
    m = []
    for i in range(n_digits):
        gen = yield_pattern(base_pattern, i+1)
        m.append(list(next(gen) for _ in range(n_digits)))
    return m


def yield_pattern(base_pattern, n):
    skip = True
    while 1:
        for i in base_pattern:
            for _ in range(n):
                if skip:
                    skip = False
                    continue
                yield i


def get_cycle_time(base_pattern, n):
    cycle_time = []

    for j in range(1, n+1):
        gen = yield_pattern(base_pattern, j)
        i = 0
        pattern = []
        while 1:
            pattern.extend([next(gen) for _ in range(n)])
            if i != 0 and pattern[:n] == pattern[-n:]:
                cycle_time.append(i)
                break
            i += 1
    return lcm(cycle_time)


def lcm(a):
    _lcm = a[0]
    for x in a[1:]:
        _lcm = (_lcm * x) // math.gcd(_lcm, x)
    return _lcm



if __name__ == '__main__':
    values_str = "12345678"
    values = list(map(int, values_str))

    base_pattern = (0, 1, 0, -1)

    print(get_cycle_time(base_pattern, len(values_str)))

    base_pattern_matrix = create_base_pattern_matrix(base_pattern, len(values))

    original_values = list(values)
    for i in range(4):
        values = compute_phase(values, base_pattern_matrix)
    print()

    values_str = "".join(map(str, values))
    print(values_str)
    message_offset = values_str[:7]
    print(values_str[message_offset:message_offset+8])

