output = open('bulkWhoisInput.txt', 'w')
output.write("begin"+'\n')
with open('chilean_asn1.csv') as f:
    lines = f.read().splitlines()
    for asn in lines:
        output.write('AS'+asn+'\n')

output.write("end")
output.close()