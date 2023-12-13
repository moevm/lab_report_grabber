import csv
import os


def check_path(path):
    if not os.path.exists(path):
        raise Exception("Path of the file is Invalid")
    return


def parse_table(args):
    check_path(args['path'])
    with open(args['path'], 'r') as f:
        rows = csv.reader(f)
        table = [row for row in rows]

    table = table[args['num_header_rows']:]
    return table
