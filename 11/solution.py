from typing import *
from collections import defaultdict
import sys

# the input has to be a dag


D = sys.stdin.readlines()
graph = defaultdict(list)
for line in D:
    node, neighbors_str = line.strip().split(":")
    graph[node] = neighbors_str.split()
    # ensure all nodes are created
    graph["out"]


def toposort(graph: dict[str, list[str]]):
    # dfs then output in reverse order
    order: list[str] = []
    discovered: set[str] = set()

    def dfs(graph, discovered, order, *, node):
        for neighbor in graph[node]:
            if neighbor not in discovered:
                discovered.add(neighbor)
                dfs(graph, discovered, order, node=neighbor)
        order.append(node)  # node is finished

    for node in graph:
        if not node in discovered:
            discovered.add(node)
            dfs(graph, discovered, order, node=node)
    return reversed(order)


def num_paths(graph, start, end):
    topo_order = toposort(graph)
    num_paths_to_node = defaultdict(int)
    num_paths_to_node[start] = 1
    for node in topo_order:
        for neighbor in graph[node]:
            num_paths_to_node[neighbor] += num_paths_to_node[node]
    return num_paths_to_node[end]


print(num_paths(graph, "you", "out"))
