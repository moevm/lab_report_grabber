import logging
import log_config
from utils import try_work_with_file, read_csv_table


def parse_table(args):
    logging.info("Parse students table")
    table = try_work_with_file("Work with students file error", args['path'], read_csv_table)
    table = table[args['num_header_rows']:]
    return table
