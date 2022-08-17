from openpyxl import load_workbook
from graphlib import TopologicalSorter
from dependencies import dependencies

def formula(node, wb):
    sheet, n = node.split('!')
    sheet = sheet.replace("'", '')
    return wb[sheet][n].value

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

wb = load_workbook('Hoja simplificada calculo anual.xlsx')
graph = build(['RESULTADOS ANÁLISIS CONSUMO!B21'], wb)

 #print(graph)
ts = TopologicalSorter(graph)
x = tuple(ts.static_order())
x = [(i, formula(i, wb)) for i in x]
#print(x)

for k in x:
    print(f';{k[0]};{k[1]}')