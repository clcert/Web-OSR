# this will take an input of AS numbers, ip blocks, for example:
# 6429,200.32.178.0/23
# 6429,200.32.182.0/23
# 6471,131.0.108.0/24
# 6471,131.0.109.0/24

# the output will be a file of format:
# <number> <\t> <comma separated ips> <\n>
print("running group_blocks.py")
output = open('grouped_blocks.txt', 'w')
with open('ip_per_asn1.csv') as f:
    lines = f.read().splitlines()
    current = '0'
    aux = ''
    for line in lines:  # at this point line is actually a line.
        pair = line.split(',')
        if pair[0] != current:  #in this case we have to save the previous number with its blocks
            if current != '0':
                output.write(current+'\t'+aux+'\n')
            current = pair[0]
            aux = pair[1]
        else:
            aux = aux + ',' + pair[1]
    output.write(current + '\t' + aux + '\n')
print('group_blocks.py script finished')
