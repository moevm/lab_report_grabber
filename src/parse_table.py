import logging

from src.config import get_config
from src.utils import try_work_with_file, read_csv_table

cfg = get_config()

def parse_table(args: dict) -> list[list[str]]:
    logging.info(cfg['Info']['parse_table'].format(where='local directory'))
    table = try_work_with_file(cfg['Error']['file'].format(name='students table'), args['path'], read_csv_table)
    table = table[args['num_header_rows']:]
    return table


def find_col_for_name(args: dict, name: str) -> int:
    table = try_work_with_file(cfg['Error']['file'].format(name='students table'), args['path'], read_csv_table)
    for row in table[:args['num_header_rows']]:
        for i in range(len(row)):
            if row[i] == name:
                return i + 1

    logging.error(cfg['Error']['not_found_named_col'])
    exit(0)
