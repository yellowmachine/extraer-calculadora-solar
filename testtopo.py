from graphlib import TopologicalSorter

graph = {"D": ["B", "C"], "C": ["A"], "B": ["A"]}
ts = TopologicalSorter(graph)

print(tuple(ts.static_order()))