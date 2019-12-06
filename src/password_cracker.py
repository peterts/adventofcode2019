def is_valid_password(num):
    num_str = str(num)
    if len(num_str) != 6:
        return False

    prev_i = -1

    n_in_sequence = 0
    sequences = {}

    for c in num_str:
        i = int(c)
        if i < prev_i:
            return False
        if prev_i == i:
            n_in_sequence += 1
        else:
            if n_in_sequence > 0 and sequences.get(i, -1) < n_in_sequence:
                sequences[prev_i] = n_in_sequence
            n_in_sequence = 0
        prev_i = i

    if n_in_sequence > 0 and sequences.get(i, -1) < n_in_sequence:
        sequences[prev_i] = n_in_sequence

    if not sequences:
        return False
    return any(x == 1 for x in sequences.values())


if __name__ == '__main__':
    c = 0
    for n in range(245318, 765748):
        if is_valid_password(n):
            c += 1
    print(c)
