import re
import string
import sys
from build_ranges import get_matrixaddress

patt = re.compile(r"('?[ñÑa-zÁÉÍÓÚáéíóúA-Z0-9\s]+'?!)?(\$?[A-Z]{1,3}\$?[0-9]{1,7})(:\$?[A-Z]{1,3}\$?[0-9]{1,7})?")
vars = string.ascii_letters

def dependencies(node, wb, dimensions):
    sheet, n = node.split('!')
    f = wb[sheet][n].value
    f = str(f)
    if not f.startswith('='):
        return None, f, None, None
    return dependencies_from_formula(f, sheet, dimensions)

def dependencies_from_formula(raw, sheet_name, dimensions):
    matches = get_matches(raw)
    ret = []
    n_vars = []
    vars_ = {}

    for i, match in enumerate(matches):
        raw = replace(raw).replace(match, vars[i])

        if not '!' in match:
            match = sheet_name + '!' + match
        
        vars_[vars[i]] = match
        n_vars.append(vars[i])
        if ':' in match:
            mx = get_matrixaddress(match)
            x = len(mx)
            y = len(mx[0])            
            print(f'{match};{x};{y}')            
            match = match[:match.index(':')]
            dimensions[match] = (x, y)
        ret.append(match)

    return ret, raw, vars_, n_vars

def get_matches(t):
    done = set()
    ret = []
    i = 0
    while True:
        x = patt.search(t, i)
        if x is None:
            break
        chunk = x.string[x.start():x.end()]
        chunk = replace(chunk)
        if chunk not in done:
            ret.append(chunk)
            done.add(chunk)
        i = x.end()
    ret = [(len(x), x) for x in ret]
    ret = sorted(ret, reverse=True)
    ret = [x[1] for x in ret]
    return ret

def replace(txt):
    txt = txt.replace("'", '')
    txt = txt.replace("$", '')
    return txt
