import re
import itertools

def build(*rs):
    ret = []

    for r in rs:
        ret += build_r(r)
    merged = list(itertools.chain(*ret))
    return merged

def build_r(r):
    if ':' not in r:
        a = r.split('!')[1]
        r = r + ':' + a
    return get_matrixaddress(r)

def address2index(address):
    address = address.upper()

    strVSnum = re.compile(r'[A-Z]+')
    colstr = strVSnum.findall(address)[0]

    col = columnletter2num(colstr)
    row = int(strVSnum.split(address)[1])

    return [row, col]


def index2address(row, col):
    colname = num2columnletters(col)

    return colname + str(row)


def columnletter2num(text):
    letter_pos = len(text) - 1
    val = 0
    try:
        val = (ord(text[0].upper())-64) * 26 ** letter_pos
        next_val = columnletter2num(text[1:])
        val = val + next_val
    except IndexError:
        return val
    return val


def num2columnletters(num):
    def pre_num2alpha(num):
        if num % 26 != 0:
            num = [num // 26, num % 26]
        else:
            num = [(num - 1) // 26, 26]

        if num[0] > 26:
            num = pre_num2alpha(num[0]) + [num[1]]
        else:
            num = list(filter(lambda x: False if x == 0 else True, num))

        return num

    return "".join(list(map(lambda x: chr(x + 64), pre_num2alpha(num))))

def get_matrixaddress(address_range):
    name, add_range = address_range.split('!')
    add_range = add_range.replace('$', '')
    add_start, add_end = add_range.split(':')

    start_row, start_col = address2index(add_start)
    end_row, end_col = address2index(add_end)

    ret = []
    for row in range(start_row, end_row+1):
        inner = []
        for col in range(start_col, end_col+1):
            inner.append(name + '!' + index2address(row, col))
        ret.append(inner)

    return ret

x = build("X!A1:B2", "Y!A1")
print(x)