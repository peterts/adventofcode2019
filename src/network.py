from src.int_program import IntProgram
from src.helpers import read_comma_separated_list
from collections import defaultdict


def create_network(size, memory):
    computers = []
    for adr in range(size):
        computer = IntProgram(memory)
        computer.run([adr])
        computers.append(computer)
    return computers


def parse_output(out, all_mesages):
    for i in range(0, len(out), 3):
        adr, x, y = out[i:i+3]
        if adr == 255:
            all_messages[adr] = [[x, y]]
        else:
            all_mesages[adr].append([x, y])


def parse_output_from_all_computers(network, all_messages):
    for computer in network:
        parse_output(computer.output, all_messages)


def run_iteration(network, all_messages, prev_nat_message=None):
    if network_is_idle(all_messages) and all_messages[255]:
        message = all_messages[255][0]
        if prev_nat_message is not None and prev_nat_message[1] == message[1]:
            return message, True
        network[0].run(message)
        return message, False
    else:
        for i, computer in enumerate(network):
            if i in all_messages and len(all_messages[i]) > 0:
                message = all_messages[i].pop(0)
            else:
                message = [-1]
            computer.run(message)
        return prev_nat_message, False


def network_is_idle(all_messages):
    for key, val in all_messages.items():
        if key == 255:
            continue
        if val:
            return False
    return True


if __name__ == '__main__':
    memory = read_comma_separated_list("network.txt", int)
    network = create_network(50, memory)

    all_messages = defaultdict(list)
    prev_nat_message = None
    while 1:
        prev_nat_message, was_duplicate = run_iteration(network, all_messages, prev_nat_message)
        if was_duplicate:
            break
        parse_output_from_all_computers(network, all_messages)
    print(prev_nat_message)
