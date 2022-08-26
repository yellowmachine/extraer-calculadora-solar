from openpyxl import load_workbook
from graphlib import TopologicalSorter
from dependencies import dependencies
from translate import translate
from input import inputs
from skip import skip

values_f = {}

raw_cell = {}

dimensions = {}

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
            deps, raw, vars, n_vars = dependencies(n, wb, dimensions)
            values_f[n] = (raw, vars, n_vars)
            if deps is not None:
                ret[n] = deps
                nodes.extend([x for x in deps if not skip(x)])

    return ret

wb = load_workbook('Hoja simplificada calculo anual.xlsx')
graph = build(inputs, wb)

ts = TopologicalSorter(graph)
x = tuple(ts.static_order())

with open('schema.txt', 'w') as out:
    for k in sorted(x):
        out.write(f'{k};{formula(k, wb)}')
        out.write('\n')

total_f = set()

funcs_set = []
funcs_partial_set = []
funcs_dict = {}
count_f = 0

for k in x:
    if skip(k):
        continue
    f = ''
    _f = None
    if values_f[k][2] is not None:
        xyz = " = np.vectorize( lambda " + ",".join(values_f[k][2]) + " : " + translate(values_f[k][0][1:]) + ")"
        total_f.add(xyz)
        f = replace(k) + " = np.vectorize( lambda " + ",".join(values_f[k][2]) + " : " + translate(values_f[k][0][1:]) + ")"
        f = f + "(" + ",".join([ replace(values_f[k][1][a]) for a in values_f[k][2]]) + ")"
        _f = "return " + translate(values_f[k][0][1:])
        if _f not in funcs_partial_set:
            if "MAX" in f or "MIN" in f or "AVERAGE" in f or "SUM" in f or "SUMIF" in f or "SUMIFS" in f:
                _f2 = f'def f_{count_f}({",".join(values_f[k][2])}):' + "\n    " + _f
            else:
                _f2 = "@np.vectorize\n" + f'def f_{count_f}({",".join(values_f[k][2])}):' + "\n    " + _f
            funcs_partial_set.append(_f)
            count_f += 1
            funcs_set.append(_f2)
            funcs_dict[_f] = count_f
        
    if _f is None:
        c = replace(k)
    else:
        c = str(funcs_dict[_f])
    s, r = k.split('!')
    r = r.split(':')[0]
    print(f'{"f_" + c};{replace(k)};{values_f[k][0]};{replace(values_f[k][1])};{values_f[k][2]};{values_f[k][1]};{k}{wb[s][r].value}')
        
#for f in total_f:
#    print(f)

for f in funcs_set:
    print(f + "\n")

print(len(total_f))

for k in graph:
    dim = []
    for x in graph[k]:
        try:
            dim.append(dimensions[x])
        except:
            dim.append(x + ":?")
    print(k, dim)

#print(dimensions)