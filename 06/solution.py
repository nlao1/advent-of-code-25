from typing import *
from functools import reduce

example: str = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


def calculate(numbers, operations):
    results: list[int] = []
    for i, operation in enumerate(operations):

        if operation == "*":
            results.append(reduce(lambda acc, x: acc * x, numbers[i]))
        elif operation == "+":
            results.append(sum(numbers[i]))
    return sum(results)


# in this problem, parsing is separate for each part
def part1(s: list[str]):
    num_problems = len(s[0].split())
    numbers_in_problems: list[list[int]] = [[] for _ in range(num_problems)]
    operations = []
    for line in s:
        operands = [operand.strip() for operand in line.strip().split()]
        if operands[0] == "*" or operands[0] == "+":  #  done
            operations.extend(operands)
        else:
            for i, num_str in enumerate(operands):
                numbers_in_problems[i].append(int(num_str))
    return calculate(numbers_in_problems, operations)


def part2(s: list[str]):
    # key idea: the operator is at the start of each column, find the indices of
    # operators, then use that to determine which numbers to read
    number_lines, operator_line = s[:-1], s[-1]
    number_lines = [line.strip("\n") for line in number_lines]
    operator_line = operator_line.strip()
    column_start_idxs = [
        i for i in range(len(operator_line)) if operator_line[i] != " "
    ]
    num_cols = len(column_start_idxs)

    def get_column_spaces_preserved(line, col_idx):
        if col_idx == num_cols - 1:
            column_start = column_start_idxs[col_idx]
            return line[column_start:]
        else:
            column_start = column_start_idxs[col_idx]
            next_column_start = column_start_idxs[col_idx + 1]
            return line[column_start : next_column_start - 1]

    parsed_numbers_in_cols: list[list[int]] = []
    for col_idx in range(num_cols):
        lines_for_col: list[str] = [
            get_column_spaces_preserved(line, col_idx) for line in number_lines
        ]
        col_width = len(lines_for_col[0])
        numbers = []
        for idx_in_col in range(col_width):
            vertical_slice: list[str] = [
                line[idx_in_col] for line in lines_for_col
            ]  # length 1 strings
            numbers.append(int("".join(vertical_slice)))
        parsed_numbers_in_cols.append(numbers)
    return calculate(parsed_numbers_in_cols, operator_line.split())


example_input = example.splitlines()
puzzle_input = open("input.txt").readlines()
print(part1(example_input))
print(part1(puzzle_input))
print(part2(example_input))
print(part2(puzzle_input))
