_skip = [
        "CALCULOS!T8020", 
        "CALCULOS!T7300", "CALCULOS!T6555", "CALCULOS!T5835",
        "CALCULOS!T5091", "CALCULOS!T4347", "CALCULOS!T3627", "CALCULOS!T2883",
        "CALCULOS!T2163", "CALCULOS!T1420", "CALCULOS!T748"
]

def skip(k):
    return k.startswith("CALCULOS!Y") and k != 'CALCULOS!Y4'