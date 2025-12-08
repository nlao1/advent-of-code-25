from typing import *
from collections import defaultdict

example: str = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

testing: str = """...S...
.......
...^...
.......
....^..
.......
.......
"""


def part1(rows: list[str]):
    rows = [row.strip() for row in rows]
    first_row = rows[0]
    beam_start_col = first_row.index("S")  # 0-indexed
    running_cols = set([beam_start_col])
    num_times_split = 0
    for row in rows[2::2]:
        splitter_idx = 0
        next_running_cols = set(running_cols)
        while (splitter_idx := row.find("^", splitter_idx + 1)) != -1:
            if splitter_idx in running_cols:
                num_times_split += 1
                next_running_cols.add(splitter_idx - 1)
                next_running_cols.add(splitter_idx + 1)
                next_running_cols.remove(splitter_idx)
        running_cols = next_running_cols
    return num_times_split


def part2(rows: list[str]):
    rows = [row.strip() for row in rows]
    first_row = rows[0]
    beam_start_col = first_row.index("S")  # 0-indexed
    running_cols = defaultdict(int)
    running_cols[beam_start_col] = 1
    for row in rows[2::2]:
        # print(row, {k: v for k, v in running_cols.items() if v > 0})
        splitter_idx = 0
        next_running_cols = running_cols.copy()
        while (splitter_idx := row.find("^", splitter_idx + 1)) != -1:
            if splitter_idx in running_cols:
                num_paths = running_cols[splitter_idx]
                next_running_cols[splitter_idx - 1] += num_paths
                next_running_cols[splitter_idx + 1] += num_paths
                next_running_cols[splitter_idx] -= num_paths
        running_cols = next_running_cols
    return sum(running_cols.values())


print(part1(example.splitlines()))
print(part1(open("input.txt").readlines()))
print(part2(example.splitlines()))
print(part2(open("input.txt").readlines()))
