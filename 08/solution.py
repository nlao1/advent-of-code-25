from typing import *
import math
from itertools import combinations


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


def euclidean_distance(p1: tuple[int, int, int], p2: tuple[int, int, int]):
    return math.sqrt((p1[2] - p2[2]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[0] - p2[0]) ** 2)


class DisjointSet:
    """
    Disjoint set with union by rank and path compression. Union by size would
    have been better but I don't know how it works
    """

    def __init__(self, points):
        self.n = len(points)
        self.ranks = {point: 0 for point in points}
        self.parents = {point: point for point in points}

    def find(self, n):
        if n != self.parents[n]:
            self.parents[n] = self.find(self.parents[n])
        return self.parents[n]

    def union(self, n1, n2):
        parent1 = self.find(n1)
        parent2 = self.find(n2)
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
    graph = {point: set() for point in points}
    point_pairs = list(combinations(points, 2))
    uf = DisjointSet(points)

    for point1, point2 in sorted(
        point_pairs, key=lambda pair: euclidean_distance(pair[0], pair[1])
    )[:connect_n_closest]:
        if uf.find(point1) != uf.find(point2):
            uf.union(point1, point2)
            graph[point1].add(point2)
            graph[point2].add(point1)

    discovered = set()

    def subtree_size(graph, point):
        discovered.add(point)
        size = 1
        for neighbor in graph[point]:
            if not neighbor in discovered:
                discovered.add(neighbor)
                size += subtree_size(graph, neighbor)
        return size

    tree_sizes = []
    for point in points:
        if not point in discovered:
            tree_sizes.append(subtree_size(graph, point))
    tree_sizes_descending = sorted(tree_sizes, reverse=True)
    return (
        tree_sizes_descending[0] * tree_sizes_descending[1] * tree_sizes_descending[2]
    )


def part2(points: list[tuple[int, int, int]]):
    point_pairs = list(combinations(points, 2))
    uf = DisjointSet(points)

    num_connected = 0
    for point1, point2 in sorted(
        point_pairs, key=lambda pair: euclidean_distance(pair[0], pair[1])
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
