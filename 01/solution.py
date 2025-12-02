from typing import TextIO

example: str = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def parse(s: list[str] | TextIO):
    turns = []
    for line in s:
        line = line.strip()
        dir, amt = line[:1], line[1:]
        amt = int(amt)
        turns.append((dir, amt))
    return turns


def part1(turns: list[tuple[str, int]]) -> int:
    pos = 50
    sum = 0
    for dir, amt in turns:
        if dir == "L":
            pos -= amt
        else:
            pos += amt
        pos %= 100
        if pos == 0:
            sum += 1
    return sum


def part2(turns: list[tuple[str, int]]) -> int:
    pos = 50
    sum = 0
    next_pos = 0
    for dir, amt in turns:
        hundreds, remainder = amt // 100, amt % 100
        sum += hundreds
        if remainder != 0:
            next_pos = pos - remainder if dir == "L" else pos + remainder
            if (
                (next_pos < 0 and pos > 0)
                or (next_pos > 100 and pos < 100)
                or next_pos % 100 == 0
            ):
                sum += 1
        pos = next_pos % 100
    return sum


if __name__ == "__main__":
    # print(part1(parse(example.splitlines())))
    # print(part1(parse(open("input.txt"))))
    print(part2(parse(example.splitlines())))
    print(part2(parse(open("input.txt"))))
