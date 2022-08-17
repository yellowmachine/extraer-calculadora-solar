import re
import string

patt = re.compile(r"('?[ñÑa-zÁÉÍÓÚáéíóúA-Z0-9\s]+'?!)?(\$?[A-Z]{1,3}\$?[0-9]{1,7})(:\$?[A-Z]{1,3}\$?[0-9]{1,7})?")
vars = string.ascii_letters

def dependencies(node, wb):
    sheet, n = node.split('!')
    f = wb[sheet][n].value
    f = str(f)
    if not f.startswith('='):
        return None, None, None
    return dependencies_from_formula(f, sheet)

def dependencies_from_formula(raw, sheet_name):
    matches = get_matches(raw)
    ret = []
    vars_ = {}

    for i, match in enumerate(matches):
        raw = replace(raw).replace(match, vars[i])
        vars_[vars[i]] = match
        if not '!' in match:
            match = sheet_name + '!' + match
        if ':' in match:
            match = match[:match.index(':')]
        ret.append(match)

    return ret, raw, vars_

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
    return ret

def replace(txt):
    txt = txt.replace("'", '')
    txt = txt.replace("$", '')
    return txt
