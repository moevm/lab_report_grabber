import logging
import log_config
import csv


def parse_table(args):
    logging.info("Parse students table")
    try:
        with open(args['path'], 'r') as f:
            table = list(csv.reader(f))
    except Exception as e:
        print(f"Work with students file error: {e}")
        exit(0)

    table = table[args['num_header_rows']:]
    return table
