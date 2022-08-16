from openpyxl import load_workbook
from graphlib import TopologicalSorter
from dependencies import dependencies

def build(nodes, wb):
    ret = {}

    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in ret:
            deps = dependencies(n, wb)
            if deps is not None:
                ret[n] = deps
                nodes.extend(deps)

    return ret

wb = load_workbook('abc.xlsx')
graph = build(['Hoja1!A2'], wb)
ts = TopologicalSorter(graph)
print(tuple(ts.static_order()))
