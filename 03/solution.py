from typing import *

example: str = """987654321111111
811111111111119
234234234234278
818181911112111"""


def parse(s: list[str]):
    return [line.strip() for line in s]


def max_joltage_part_1(bank: list[int]):
    max_start_battery: Optional[int] = None
    curr_max_joltage: Optional[int] = None
    for i, battery_joltage in enumerate(bank):
        if i == len(bank) - 1:
            break
        if max_start_battery is None or battery_joltage > max_start_battery:
            candidate = 10 * battery_joltage + max(bank[i + 1 :])
            if curr_max_joltage is None or candidate > curr_max_joltage:
                max_start_battery = battery_joltage
                curr_max_joltage = candidate
    return curr_max_joltage


def max_joltage(bank: list[int], necessary_remaining):
    # i think this has optimal substructure
    # find the leftmost max number that leaves at least `necessary_remaining`,
    # then recursively call on the slice after
    if necessary_remaining == 1:
        return max(bank)
    curr_max = -1
    curr_max_index = -1
    for i in range(len(bank) - necessary_remaining, -1, -1):
        joltage = bank[i]
        if curr_max is None or joltage >= curr_max:
            curr_max = joltage
            curr_max_index = i
    return curr_max * (10 ** (necessary_remaining - 1)) + max_joltage(
        bank[curr_max_index + 1 :], necessary_remaining - 1
    )


def part1(banks: list[str]):
    return sum(max_joltage_part_1([int(x) for x in bank]) for bank in banks)


def part2(banks: list[str]):
    return sum(max_joltage([int(x) for x in bank], 12) for bank in banks)


example_input = parse(example.splitlines())
puzzle_input = parse(open("input.txt").readlines())
print(part1(example_input))
print(part1(puzzle_input))
print(part2(example_input))
print(part2(puzzle_input))
