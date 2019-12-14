from functools import partial
from src.helpers import read_comma_separated_list
from collections import defaultdict

STATE_RUNNING = 0
STATE_WAITING = 1
STATE_HALTED = 2


class IntProgram:
    def __init__(self, memory, n_params=3, n_op_digits=2, always_move_pointer=False):
        self.n_params = n_params
        self.n_op_digits = n_op_digits
        self.always_move_pointer = always_move_pointer

        self.memory = defaultdict(int, enumerate(memory))
        self.relative_base = 0
        self.pointer = 0
        self.output = []
        self.state = STATE_WAITING

        self.inp = None
        self.param_modes = None
        self.operations = self.init_operations()

    def init_operations(self):
        return {opcode: partial(method, self) for opcode, method in operations}

    def restart(self):
        self.pointer = 0
        self.relative_base = 0
        self.state = STATE_WAITING

    def run(self, inp=None):
        if inp is None:
            inp = []

        self.inp = list(inp)
        self.output = []
        self.param_modes = [0] * self.n_params

        self.state = STATE_RUNNING

        operator, self.param_modes = self.get_operator_and_param_modes()
        while self.state == STATE_RUNNING:
            self.operations[operator]()
            operator, self.param_modes = self.get_operator_and_param_modes()

        return self

    def get_param(self, j):
        return self.memory[self.param_address(j)]

    def set_param(self, j, value):
        adr = self.param_address(j)
        self.memory[adr] = value
        return adr

    def param_address(self, j):
        i = self.pointer + j + 1
        if self.param_modes[j] == 0:
            return self.memory[i]
        elif self.param_modes[j] == 1:
            return i
        elif self.param_modes[j] == 2:
            return self.memory[i] + self.relative_base

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
    self.move_pointer(self.set_param(0, self.inp.pop(0)), 2)


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


if __name__ == '__main__':
    memory = read_comma_separated_list("int_program3.txt", int)
    program = IntProgram(memory)
    program.run([2])
    print(program.output)
