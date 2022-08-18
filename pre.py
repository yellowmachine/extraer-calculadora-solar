from openpyxl import load_workbook
from graphlib import TopologicalSorter
from dependencies import dependencies
from translate import translate

values_f = {}

def formula(n, wb):
    sheet, r = n.split('!')
    return wb[sheet][r].value

def _replace(txt):
    txt = txt.replace("!", '__')
    txt = txt.replace("ñ", 'ny')
    txt = txt.replace("Ñ", 'Ny')
    txt = txt.replace("á", 'a')
    txt = txt.replace("é", 'e')
    txt = txt.replace("í", 'i')
    txt = txt.replace("ó", 'o')
    txt = txt.replace("ú", 'u')
    txt = txt.replace("Á", 'A')
    txt = txt.replace("É", 'E')
    txt = txt.replace("Í", 'I')
    txt = txt.replace("Ó", 'O')
    txt = txt.replace("Ú", 'U')
    txt = txt.replace(" ", '_')

    txt = txt.split(':')[0]

    return txt

def replace(o):
    if o.__class__ == dict:
        return {k: _replace(v) for k, v in o.items()}
    elif o is not None:
        return _replace(o)
    else:
        return None

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
    f = ''
    if values_f[k][2] is not None:
        f = replace(k) + " = np.vectorize( lambda " + ",".join(values_f[k][2]) + " : " + translate(values_f[k][0][1:]) + ")"
        f = f + "(" + ",".join([ replace(values_f[k][1][a]) for a in values_f[k][2]]) + ")"
    print(f'{f};{replace(k)};{values_f[k][0]};{replace(values_f[k][1])};{values_f[k][2]}')
    
with open('schema.txt', 'w') as out:
    for k in sorted(x):
        out.write(f'{k};{formula(k, wb)}')
        out.write('\n')