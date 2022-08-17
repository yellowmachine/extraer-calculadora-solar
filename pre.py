from openpyxl import load_workbook
from graphlib import TopologicalSorter
from dependencies import dependencies

def formula(node, wb):
    sheet, n = node.split('!')
    sheet = sheet.replace("'", '')
    return wb[sheet][n].value

values_f = {}

def build(nodes, wb):
    ret = {}

    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in ret:
            deps, raw, vars = dependencies(n, wb)
            values_f[n] = (raw, vars)
            if deps is not None:
                ret[n] = deps
                nodes.extend(deps)

    return ret

wb = load_workbook('Hoja simplificada calculo anual.xlsx')
graph = build(['RESULTADOS ANÁLISIS CONSUMO!B21'], wb)

ts = TopologicalSorter(graph)
x = tuple(ts.static_order())
print(x)
resultado = [(k, v) for (k, v) in values_f.items() if v[0] is not None]
for k in resultado:
    print(k)
#x = [(i, formula(i, wb)) for i in x]

#for k in x:
#    print(f';{k[0]};{k[1]}')