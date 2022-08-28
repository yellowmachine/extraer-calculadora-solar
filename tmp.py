structure = {}

for line in open("schema_with_types.csv"):
    if line.endswith(';*\n'):
        line = line[:-3]
    campos = line.split(";")
    first = campos[0]
    if first.startswith('#'):
        continue
    longitud = len(campos)
    if longitud == 3:
        structure[campos[1]] = first

for line in open('schema_topo.csv'):
    line = line[:-1]
    k = line.split(';')[0]
    if k in structure:
        print(structure[k] + ';' + line)
    else:
        print(line)