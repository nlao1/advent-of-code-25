from ortools.linear_solver import pywraplp
from collections import deque
from typing import *
import sys

D = sys.stdin.readlines()
lines = [line.strip().split() for line in D]


def parse_line(line: list[str]):
    target_state = tuple((True if c == "#" else False) for c in line[0][1:-1])
    buttons = line[1:-1]
    buttons = [
        tuple([int(button_toggled) for button_toggled in button[1:-1].split(",")])
        for button in buttons
    ]
    target_flips = tuple(
        int(button_toggled) for button_toggled in line[-1][1:-1].split(",")
    )
    # to be used in part 2
    return (target_state, buttons, target_flips)


def bfs(initial_state, target_state, *, get_edges):
    Q = deque()
    Q.append(initial_state)
    discovered = {initial_state}
    parents = {}

    while True:  # break out when something in discovered found again
        next = Q.popleft()
        for neighbor in get_edges(next):
            if neighbor not in discovered:
                parents[neighbor] = next
                discovered.add(neighbor)
                if neighbor == target_state:
                    return parents
                else:
                    Q.append(neighbor)


def trace_path_length(parents, target_state):
    node = target_state
    length = 1
    while (node := parents[node]) in parents:
        length += 1
    return length


def min_number_presses(target_state, buttons):
    initial_state = tuple(False for _ in target_state)

    def edges(state):
        return [
            tuple(not (b) if i in button else b for i, b in enumerate(state))
            for button in buttons
        ]

    parents = bfs(
        initial_state,
        target_state,
        get_edges=edges,
    )
    return trace_path_length(parents, target_state)


def min_number_presses_joltage(buttons, target_state):
    # basically a linear algebra problem
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return
    inf = solver.infinity()
    button_counts = [solver.IntVar(0.0, inf, str(i)) for i in range(len(buttons))]

    # add constraints that dot product must equal target state
    for counter_idx, target_presses in enumerate(target_state):
        sum_of_counter_values_at_idx = sum(
            button_count if counter_idx in buttons[button_idx] else 0
            for button_idx, button_count in enumerate(button_counts)
        )
        solver.Add(target_presses <= sum_of_counter_values_at_idx)
        solver.Add(target_presses >= sum_of_counter_values_at_idx)

    # optimize for least presses
    solver.Minimize(sum(button_counts))
    solver.Solve()
    return int(solver.Objective().Value())


print(sum(min_number_presses(*parse_line(line)[:2]) for line in lines))
print(sum(min_number_presses_joltage(*parse_line(line)[1:]) for line in lines))
