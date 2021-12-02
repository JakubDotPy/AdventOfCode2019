import argparse
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
100756
"""


def get_fuel(mass):
    return mass // 3 - 2


def get_fuel_recursive(mass):
    total_fuel = 0
    while True:
        sub_result = get_fuel(mass)
        if sub_result > 0:
            total_fuel += sub_result
            mass = sub_result
        else:
            return total_fuel


def compute(s: str) -> int:
    nums = [int(n) for n in s.splitlines()]
    return sum(map(get_fuel_recursive, nums))


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 50346),
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
