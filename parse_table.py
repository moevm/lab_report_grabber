from check_path import check_path
import csv


def parse_table(args):
    check_path(args['path'])
    with open(args['path'], 'r') as f:
        table = list(csv.reader(f))

    table = table[args['num_header_rows']:]
    return table
