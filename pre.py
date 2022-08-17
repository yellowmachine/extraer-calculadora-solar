from openpyxl import load_workbook
from graphlib import TopologicalSorter
from dependencies import dependencies

values_f = {}

def build(nodes, wb):
    ret = {}

    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in ret:
            deps, raw, vars, n_vars = dependencies(n, wb)
            values_f[n] = (raw, vars, n_vars)
            if deps is not None:
                ret[n] = deps
                nodes.extend(deps)

    return ret

wb = load_workbook('Hoja simplificada calculo anual.xlsx')
graph = build(['RESULTADOS ANÁLISIS CONSUMO!B21'], wb)

ts = TopologicalSorter(graph)
x = tuple(ts.static_order())
#print(x)

for k in x:
    print(f'{k};{values_f[k][0]};{values_f[k][1]};{values_f[k][2]}')
    