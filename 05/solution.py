from typing import *

example: str = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

fooling_example: str = """100-101
1-2
3-5
4-9
4-8
4-7
"""


def parse(s: list[str]):
    ranges = []
    ranges_all_found = False
    numbers = []
    for line in s:
        if len(line.strip()) == 0:
            ranges_all_found = True
        elif not ranges_all_found:
            start, end = line.strip().split("-")
            ranges.append((int(start), int(end)))
        else:
            numbers.append(int(line.strip()))
    return ranges, numbers


def part1(ranges: list[tuple[int, int]], numbers: list[int]):
    def number_in_ranges(num):
        for range_start_inclusive, range_end_inclusive in ranges:
            if num >= range_start_inclusive and num <= range_end_inclusive:
                return True
        return False

    return sum(1 if number_in_ranges(num) else 0 for num in numbers)


# somehow i sorted yet made the mistake of using `ranges` twice
def part2(ranges: list[tuple[int, int]]):
    # goal is to find all numbers in any range
    # idea: sorting by either start or end is probably useful
    ranges_increasing_start = sorted(ranges, key=lambda x: x[0])
    finalized_ranges = []
    current_range: tuple[int, int] = ranges_increasing_start[
        0
    ]  # range currently being considered to combine

    for range_start, range_end in ranges_increasing_start[1:]:
        if range_start <= current_range[1] + 1:  # so adjacent ranges can merge
            current_range = (current_range[0], max(range_end, current_range[1]))
        elif range_start > current_range[1]:
            finalized_ranges.append(current_range)
            current_range = (range_start, range_end)
        else:
            raise ValueError(
                "unexpected state",
                finalized_ranges,
                current_range,
                (range_start, range_end),
            )
    finalized_ranges.append(current_range)

    return sum(
        range_end - range_start + 1 for range_start, range_end in finalized_ranges
    )


example_input = parse(example.splitlines())
puzzle_input = parse(open("input.txt").readlines())

print(part1(*example_input))
print(part1(*puzzle_input))
print(part2(example_input[0]))
print(part2(parse(fooling_example.splitlines())[0]))
print(part2(puzzle_input[0]))
