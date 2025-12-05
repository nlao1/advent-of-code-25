from typing import *

ADJACENT_OFFSETS = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
]

example: str = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def accessible_rolls(grid: list[str] | list[list[str]]):
    # len of this result of this function is the solution to pt1
    num_rows = len(grid)
    num_cols = len(grid[0])

    # each item in the list is a "row"
    def accessable(row_idx, col_idx):
        if grid[row_idx][col_idx] != "@":
            return 0
        num_rolls_in_adjacent_squares = 0
        for row_offset, col_offset in ADJACENT_OFFSETS:
            adjacent_row = row_idx + row_offset
            adjacent_col = col_idx + col_offset

            if (
                adjacent_row >= 0
                and adjacent_row < num_rows
                and adjacent_col >= 0
                and adjacent_col < num_cols
            ):
                if grid[adjacent_row][adjacent_col] == "@":
                    num_rolls_in_adjacent_squares += 1
        return 1 if num_rolls_in_adjacent_squares < 4 else 0

    return [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[row]))
        if accessable(row, col)
    ]


def part2(grid: list[str]):
    count = 0
    grid_mutable = [[x for x in row] for row in grid]
    rolls_to_remove = accessible_rolls(grid_mutable)
    while len(rolls_to_remove) > 0:
        count += len(rolls_to_remove)
        for row, col in rolls_to_remove:
            grid_mutable[row][col] = "."
        rolls_to_remove = accessible_rolls(grid_mutable)
    return count


example_input = example.splitlines()
puzzle_input = [line.strip() for line in open("input.txt").readlines()]
print(len(accessible_rolls(example_input)))
print(len(accessible_rolls(puzzle_input)))
print(part2(example_input))
print(part2(puzzle_input))
