import logging
import log_config
from utils import try_work_with_file, read_csv_table


def parse_table(args):
    logging.info("Parse students table")
    table = try_work_with_file("Work with students file error", args['path'], read_csv_table)
    table = table[args['num_header_rows']:]
    return table


def find_col_for_name(args, name):
    table = try_work_with_file("Work with students file error", args['path'], read_csv_table)
    for row in table[:args['num_header_rows']]:
        for i in range(len(row)):
            if row[i] == name:
                return i + 1

    logging.error("Not found named col")
    exit(0)
