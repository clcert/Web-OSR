print("running group_asns_to_names.py")
output = open('chilean_asn_name', 'w')
with open('chilean_asn1.csv') as fnumber:
    lines = fnumber.readlines()
    with open('asn_names.txt') as fnames:
        linesN = fnames.readlines()[1:]
        zipped_result = zip(lines, linesN)
        for linea in zipped_result:
            output.write(linea[0].strip('\n')+'\t'+linea[1])
output.close()
print("group_asns_to_names.py script finished")
