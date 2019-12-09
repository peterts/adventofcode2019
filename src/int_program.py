from functools import partial
from src.helpers import read_comma_separated_list

STATE_RUNNING = 0
STATE_WAITING = 1
STATE_HALTED = 2


class IntProgram:
    def __init__(self, memory, n_params=3, n_op_digits=2, always_move_pointer=False):
        self.n_params = n_params
        self.n_op_digits = n_op_digits
        self.always_move_pointer = always_move_pointer

        self.memory = list(memory)
        self.relative_base = 0
        self.pointer = 0
        self.output = []
        self.state = STATE_WAITING

        self.inp = None
        self.param_modes = None
        self.operations = self.init_operations()

    def init_operations(self):
        return {opcode: partial(method, self) for opcode, method in operations}

    def run(self, inp=None):
        if inp is None:
            inp = []

        self.inp = inp
        self.output = []
        self.param_modes = [0] * self.n_params

        self.state = STATE_RUNNING

        operator, self.param_modes = self.get_operator_and_param_modes()
        while self.state == STATE_RUNNING:
            self.operations[operator]()
            if operator == 203:
                print(self.pointer, operator)
            operator, self.param_modes = self.get_operator_and_param_modes()

        return self

    def set_memory(self, i, value):
        if len(self.memory) <= i:
            self.memory += [0] * (i - len(self.memory) + 1)
        self.memory[i] = value

    def get_from_memory(self, i):
        if i >= len(self.memory):
            return 0
        return self.memory[i]

    def get_param(self, j):
        i = self.pointer + j + 1
        if self.param_modes[j] == 0:
            i = self.get_from_memory(i)
            return self.get_from_memory(i)
        elif self.param_modes[j] == 1:
            return self.get_from_memory(i)
        elif self.param_modes[j] == 2:
            i = self.get_from_memory(i)
            return self.get_from_memory(self.relative_base + i)

    def set_param(self, j, value):
        i = self.get_from_memory(self.pointer + j + 1)
        if self.param_modes[j] == 0:
            self.set_memory(i, value)
            return i
        elif self.param_modes[j] == 2:
            self.set_memory(self.relative_base + i, value)
            return self.relative_base + i
        raise ValueError

    def get_operator_and_param_modes(self):
        operator = self.memory[self.pointer]
        opertor_str = str(operator).zfill(self.n_params + self.n_op_digits)
        return int(opertor_str[-self.n_op_digits:]), tuple(map(int, opertor_str[-self.n_op_digits - 1::-1]))

    def move_pointer(self, i_out, steps):
        if (i_out != self.pointer) or self.always_move_pointer:
            self.pointer += steps


operations = set()


def register_operation(opcode):
    def register_operation_and_return_method(operation):
        operations.add((opcode, operation))
        return operation

    return register_operation_and_return_method


@register_operation(1)
def add(self: IntProgram):
    _run_3_param_op(self, lambda x, y: x + y)


@register_operation(2)
def multiply(self: IntProgram):
    _run_3_param_op(self, lambda x, y: x * y)


@register_operation(3)
def read_inp(self: IntProgram):
    if not self.inp:
        self.state = STATE_WAITING
        return
    self.move_pointer(self.set_param(2, self.inp.pop(0)), 2)


@register_operation(4)
def write_out(self: IntProgram):
    self.output.append(self.get_param(0))
    self.pointer += 2


@register_operation(5)
def jump_if_true(self: IntProgram):
    _jump(self, True)


@register_operation(6)
def jump_if_false(self: IntProgram):
    _jump(self, False)


@register_operation(7)
def less_than(self: IntProgram):
    _run_3_param_op(self, lambda x, y: int(x < y))


@register_operation(8)
def equals(self: IntProgram):
    _run_3_param_op(self, lambda x, y: int(x == y))


@register_operation(9)
def adjust_relative_base(self: IntProgram):
    self.relative_base += self.get_param(0)
    self.pointer += 2


@register_operation(99)
def halt(self: IntProgram):
    self.state = STATE_HALTED


def _run_3_param_op(self: IntProgram, op):
    self.move_pointer(self.set_param(2, op(self.get_param(0), self.get_param(1))), 4)


def _jump(self: IntProgram, jump_if):
    self.pointer = self.get_param(1) if bool(self.get_param(0)) == jump_if else self.pointer + 3


def fix_memory(memory, wrong_opcode):
    n_instructions = {
        1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0
    }
    operator = int(str(wrong_opcode).zfill(2)[-2:])
    while wrong_opcode in memory:
        i = memory.index(wrong_opcode)
        memory = memory[:i] + memory[i+n_instructions[operator]:]
    return memory


if __name__ == '__main__':
    memory = read_comma_separated_list("int_program3.txt", int)
    # memory = (109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99)
    # print(memory)

    program = IntProgram(memory)
    program.run([2])
    print(program.output)
