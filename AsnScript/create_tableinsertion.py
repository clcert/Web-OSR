print("running create_tableinsertion.py")
output = open('insert_asn_data.sql', 'w')
with open('grouped_asn_names_blocks') as f:
    lines = f.read().splitlines()
    for line in lines:  # at this point line is actually a line from the file
        my_tuple = line.split('\t')
        # INSERT INTO asn VALUES ('thenumber', 'thename', '{theips}');
        try:
            if my_tuple[2]:
                output.write(
                    "INSERT INTO asn VALUES ('" + my_tuple[0] + "', '" + my_tuple[1] + "', '{" + my_tuple[2] + "}');" + '\n')
        except IndexError:
            output.write(
                "INSERT INTO asn VALUES ('" + my_tuple[0] + "', '" + my_tuple[1] + "');" + '\n')
print("create_tableinsertion.py script finished")