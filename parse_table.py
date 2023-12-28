from check_path import check_path
import csv


def parse_table(args):
    check_path(args['path'])
    try:
        with open(args['path'], 'r') as f:
            table = list(csv.reader(f))
    except:
        raise Exception("Work with file error")

    table = table[args['num_header_rows']:]
    return table
