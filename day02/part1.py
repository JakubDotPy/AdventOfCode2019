import argparse
import operator
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
1,9,10,3,2,3,11,0,99,30,40,50
"""


class Computer:

    # opcode methods
    def halt(self, *args):
        raise StopIteration

    opcode_operations = {
        99: halt,
        1 : operator.add,
        2 : operator.mul
        }

    def __init__(self, memory):
        self.memory = memory
        self.pointer = 0

        self.stop_condition = False

    def _next_instruction(self):
        try:
            instruction = self.memory[self.pointer:self.pointer + 4]
            self.pointer += 4
            return instruction
        except IndexError:
            return [99, None, None, None]

    def _process_instruction(self, instruction):
        opcode, from_one, from_two, store_to = instruction
        try:
            self.memory[store_to] = self.opcode_operations[opcode](self.memory[from_one], self.memory[from_two])
        except (StopIteration, IndexError):
            self.stop_condition = True

    def run(self):
        while not self.stop_condition:
            self._process_instruction(self._next_instruction())

    @property
    def result(self):
        return self.memory[0]


def compute(s: str) -> int:
    # parse numbers
    nums = [int(n) for n in s.split(',')]

    c = Computer(memory=nums)
    c.run()
    return c.result


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 3500),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
