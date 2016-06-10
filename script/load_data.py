import argparse
import json

import datetime
import os

import psycopg2
import sys

TMPFILE_NAME = 'tmpfile.txt'
EMPTY_SCAN = ['ip', 'date', 'error', 'schema_version']
HTTP_PRODUCT = "INSERT INTO http_product SELECT %s AS port, date, data#>>'{metadata, service, product}' AS product, " \
               "data#>>'{metadata, service, version}' AS version, COUNT (*) AS total FROM %s " \
               "WHERE data#>>'{metadata, service, product}'!='' AND date='%s' " \
               "GROUP BY port, date, product, version;"
HTTP_OS = "INSERT INTO http_os SELECT %s AS port, date, data#>>'{metadata, device, os}' AS os, " \
          "data#>>'{metadata, device, os_version}' AS version, COUNT (*) AS total FROM %s " \
          "WHERE data#>>'{metadata, device, os}'!='' AND date='%s' GROUP BY port, date, os, version;"
HTTP_TYPE = "INSERT INTO http_type SELECT %s AS port, date, data#>>'{metadata, device, type}' AS type, " \
            "COUNT (*) AS total FROM %s WHERE data#>>'{metadata, device, type}'!='' AND date='%s' GROUP BY port, date, type;"


def escape_string(string):
    return string.replace('\\u0000', '').replace('\\\\\\', '\\').replace('\\', '\\\\')


def parse_date(date_string):
    if date_string.count('/') == 2:
        day, month, year = date_string.split('/')
        return year + '-' + month + '-' + day
    return date_string


def argument_parser():
    parser = argparse.ArgumentParser(description='Insert a data into postgres database')

    parser.add_argument('--user', help='Database user', required=True)
    parser.add_argument('--password', help='Database user password', required=True)
    parser.add_argument('--host', help='Database host', default='localhost', required=False)
    parser.add_argument('--dbname', help='Database name', required=True)
    parser.add_argument('--dbtable', help='Database table', required=False)
    parser.add_argument('--port', help='Port scaned', required=True)
    parser.add_argument('--date', help='Scan date', required=True)
    parser.add_argument('--filename', help='File to insert into database', required=True)
    parser.add_argument('--scan', help='Insert scan data', action='store_true', required=False)
    parser.add_argument('--zmap', help='Insert zmap log', action='store_true',  required=False)
    parser.add_argument('--http', help='Insert data of http protocol', action='store_true', required=False)

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
        csv_line = '%s; %s; %s; %s; %s; %s\n' % (json_line.get("port"), json_line.get("date"), json_line.get("time"),
                                         json_line.get("send"), json_line.get("recv"), json_line.get("hits"))
        writer.write(csv_line)

    data_file.close()
    writer.close()


def http(cur, port, dbtable, date):
    query_product = HTTP_PRODUCT % (port, dbtable, date)
    cur.execute(query_product)

    query_os = HTTP_OS % (port, dbtable, date)
    cur.execute(query_os)

    query_type = HTTP_TYPE % (port, dbtable, date)
    cur.execute(query_type)


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

    if args.scan:
        cur.copy_from(f, args.dbtable, columns=('ip', 'date', 'success', 'data'), sep=";")
    elif args.zmap:
        cur.copy_from(f, 'zmap_log', columns=('port', 'date', 'time', 'send', 'recv', 'hits'), sep=";")

    if args.http:
        http(cur, args.port, args.dbtable, parse_date(args.date))

    f.close()
    conn.commit()
    os.remove(TMPFILE_NAME)