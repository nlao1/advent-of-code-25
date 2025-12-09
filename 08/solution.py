from typing import *
import math
from itertools import combinations
from collections import defaultdict


example: str = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


class DisjointSet:
    """
    Disjoint set with union by rank and path compression. Union by size would
    have been better but I don't know how it works.
    """

    def __init__(self, nodes):
        self.ranks = {point: 0 for point in nodes}
        self.parents = {point: point for point in nodes}

    def find(self, node):
        if node != self.parents[node]:
            self.parents[node] = self.find(self.parents[node])
        return self.parents[node]

    def union(self, node1, node2):
        parent1 = self.find(node1)
        parent2 = self.find(node2)
        rank1 = self.ranks[parent1]
        rank2 = self.ranks[parent2]
        if parent1 == parent2:
            return
        elif rank1 > rank2:
            self.parents[parent2] = parent1
        else:
            self.parents[parent1] = parent2
            if rank1 == rank2:
                self.ranks[parent1] += 1


def parse(s: list[str]):
    points: list[tuple[int, int, int]] = []
    for line in s:
        x, y, z = line.strip().split(",")
        points.append((int(x), int(y), int(z)))
    return points


def part1(points: list[tuple[int, int, int]], *, connect_n_closest):
    point_pairs = list(combinations(points, 2))
    uf = DisjointSet(points)

    for point1, point2 in sorted(
        point_pairs,
        key=lambda pair: math.dist(pair[0], pair[1]),
    )[:connect_n_closest]:
        if uf.find(point1) != uf.find(point2):
            uf.union(point1, point2)
    sizes = defaultdict(int)
    for point in points:
        sizes[uf.find(point)] += 1
    sizes_sorted = sorted(sizes.values())
    return sizes_sorted[-1] * sizes_sorted[-2] * sizes_sorted[-3]


def part2(points: list[tuple[int, int, int]]):
    point_pairs = list(combinations(points, 2))
    uf = DisjointSet(points)

    num_connected = 0
    for point1, point2 in sorted(
        point_pairs, key=lambda pair: math.dist(pair[0], pair[1])
    ):
        if uf.find(point1) != uf.find(point2):
            uf.union(point1, point2)
            num_connected += 1
        if num_connected == len(points) - 1:
            break
    return point1[0] * point2[0]


example_input = parse(example.splitlines())
puzzle_input = parse(open("input.txt").readlines())
print(part1(example_input, connect_n_closest=10))
print(part1(puzzle_input, connect_n_closest=1000))
print(part2(example_input))
print(part2(puzzle_input))
