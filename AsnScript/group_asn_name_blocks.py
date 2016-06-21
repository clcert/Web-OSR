# this will take 2 input files. the first will contain the ASN, tab, ASN Name
# for example:
# 1296	University of Chili, CL
# 4995	Netup S.A., CL
# 6240	Chilenet Ltda., CL
# The second file will contain ASN, tab, comma separated ip blocks. for example:
# 6429	161.25.178.0/24,190.54.0.0/16,190.54.0.0/17,190.54.32.0/19

# the output will be a file of format:
# <number> <\t> <ASN Name> <\t> <comma separated ips> <\n>
# this could be done in linear time opening both files simultaneously and advancing through each line
# but i sort of dont know how to do this on python, and i'm not switching to java
# tldr: cuadratic time
print("running group_asn_name_blocks.py")
output = open('grouped_asn_names_blocks', 'w')
with open('chilean_asn_name') as fname:
    success = 'yeah'
    fname_lines = fname.read().splitlines()
    current_asn = '0'
    for fname_line in fname_lines:  # at this point fname_line is actually a line from the file
        fname_pair = fname_line.split('\t')
        with open('grouped_blocks.txt') as fblocks:
            fblocks_lines = fblocks.read().splitlines()
            for fblocks_line in fblocks_lines:
                fblocks_pair = fblocks_line.split('\t')
                if fblocks_pair[0] == fname_pair[0]:
                    output.write(fname_pair[0] + '\t' + fname_pair[1] + '\t' + fblocks_pair[1] + '\n')
                    #print fname_pair[0] + '\t' + fname_pair[1] + '\t' + fblocks_pair[1]
                    success = fname_pair[0]
                    break
        if success != fname_pair[0]:
            output.write(fname_pair[0] + '\t' + fname_pair[1] + '\n')
            #print fname_pair[0] + '\t' + fname_pair[1]
print('group_asn_name_blocks.py script finished')
