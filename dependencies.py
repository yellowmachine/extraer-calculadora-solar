import re

patt = re.compile(r"([ñÑa-zÁÉÍÓÚáéíóúA-Z0-9\s]+!)?(\$?[A-Z]{1,3}\$?[0-9]{1,7})(:\$?[A-Z]{1,3}\$?[0-9]{1,7})?")

def get_dependencies_from_formula(raw, sheet_name):
    matches = get_matches(raw)
    ret = []
    for match in matches:
        if not '!' in match:
            match = sheet_name + '!' + match
        if ':' in match:
            match = match[:match.index(':')]
        ret.append(match)
    return ret

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
    #txt = txt.replace("'", '')
    txt = txt.replace("$", '')
    #txt = txt.replace(".", '')
    #txt = txt.replace("[", '')
    #txt = txt.replace("]", '')
    return txt

c = get_dependencies_from_formula("A1:B3 + Hoja300!$Z$1", "Hoja1")
print(c)