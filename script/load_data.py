import argparse
import json
import os

import psycopg2
import sys

TMPFILE_NAME = 'tmpfile.txt'
EMPTY_SCAN = ['ip', 'date', 'error', 'schema_version']


def escape_string(string):
    return string.replace('\\u0000', '').replace('\\\\\\', '\\').replace('\\', '\\\\')


def argument_parser():
    parser = argparse.ArgumentParser(description='Insert a data into postgres database')

    parser.add_argument('--user', help='Database user', required=True)
    parser.add_argument('--password', help='Database user password', required=True)
    parser.add_argument('--host', help='Database host', default='localhost', required=False)
    parser.add_argument('--dbname', help='Database name', required=True)
    parser.add_argument('--dbtable', help='Database table', required=False)
    parser.add_argument('--filename', help='File to insert into database', required=False)
    parser.add_argument('--scan', help='Insert scan data', action='store_true', required=False)
    parser.add_argument('--zmap', help='Insert zmap log', action='store_true',  required=False)

    return parser.parse_args()


def is_empty_scan(json_line):
        if len(json_line) > 4:
            return False

        is_empty = True
        for key in EMPTY_SCAN:
            is_empty = is_empty and key in json_line

        return is_empty


def scan_data(data_file):
    writer = file(TMPFILE_NAME, 'w')

    for line in data_file:
        json_line = json.loads(line)
        csv_line = '%s; %s; %s; %s\n' % (json_line.get("ip"), json_line.get("date"), not is_empty_scan(json_line), escape_string(line.rstrip().replace(';', ',')))
        writer.write(csv_line)

    data_file.close()
    writer.close()


def zmap_data(data_file):
    writer = file(TMPFILE_NAME, 'w')

    for line in data_file:
        json_line = json.loads(line)
        csv_line = '%s; %s; %s; %s; %s; %s; %s; %s\n' % (json_line.get("port"), json_line.get("date"), json_line.get("time"),
                                         json_line.get("send"), json_line.get("send_avg"), json_line.get("recv"),
                                         json_line.get("recv_avg"), json_line.get("hits"))
        writer.write(csv_line)

    data_file.close()
    writer.close()


if __name__ == '__main__':
    args = argument_parser()
    fileData = open(args.filename)

    if args.scan:
        scan_data(fileData)
    elif args.zmap:
        zmap_data(fileData)
    else:
        fileData.close()
        sys.exit(1)

    try:
        conn = psycopg2.connect(host=args.host, database=args.dbname, user=args.user, password=args.password)
    except:
        print "Unable to connect to the database"
        sys.exit(1)

    cur = conn.cursor()

    f = open(TMPFILE_NAME)
    cur.copy_from(f, args.dbtable, columns=('ip', 'date', 'success', 'data'), sep=";")
    f.close()

    conn.commit()

    os.remove(TMPFILE_NAME)