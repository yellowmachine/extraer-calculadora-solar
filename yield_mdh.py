import numpy as np

def mdays(m):
    return (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[m]

def iterar_mdh():
    for m in range(12):
        for d in range(mdays(m)):
            for h in range(24):
                yield (m, d, h)

for x in iterar_mdh():
    print(x)

def load_mdh_from_xlsx(sheet, ini, end):
    data = sheet[ini:end]

    ret = np.full((12, 31, 24), np.nan)
    for ((m, d, h), v) in zip(iterar_mdh(), data):
        ret[m, d, h] = v

    return ret
