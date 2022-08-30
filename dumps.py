from openpyxl import load_workbook
from build_ranges import index2address, address2index

def dump_range(wb, addr, flatten=True):
    addr = addr.replace("'", "")
    sheet, rg = addr.split("!")
    r1, r2 = rg.split(":")

    values = wb[sheet][r1:r2]
    if flatten:
        ret = []
        for x in values:
            for i in x:
                ret.append(i.value)
        return ret
    else:
        return [[i.value for i in x] for x in values]

def dump_cell(wb, addr):
    addr = addr.replace("'", "")
    sheet, cell = addr.split("!")
    return wb[sheet][cell].value

def dump(wb, lista):
    ret = {}

    for addr in lista:
        if ':' in addr:
            ret[addr] = dump_range(wb, addr)
        else:
            ret[addr] = dump_cell(wb, addr)            
    return ret

def pre(z):
    a, b = z
    if b == 'm':
        x, y = a.split('!')
        row, col = address2index(y)
        row += 12
        a = x + "!" + index2address(row, col)
    elif b == 'h':
        x, y = a.split('!')
        row, col = address2index(y)
        row += 24
        a = x + "!" + index2address(row, col)
    elif b == 'mdh':
        x, y = a.split('!')
        row, col = address2index(y)
        row += 7000
        a = x + "!" + index2address(row, col)
    elif b == 'mh':
        x, y = a.split('!')
        row, col = address2index(y)
        row += 12
        col += 24
        a = x + "!" + index2address(row, col)
    return a

wb = load_workbook('Hoja simplificada calculo anual.xlsx')
skip = []

lista = [("hoja!a1", "1"), ("hoja!a2", "m"), ...]
lista = [pre(x) for x in lista if x not in skip]
dump(wb, lista)