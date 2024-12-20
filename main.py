import logging
import os

from src.log_config import set_logging_config
from src.get_students import get_students
from src.parse_table import parse_table
from src.parse_github import parse_repo
from src.fill_table import write_rows, write_missing_studens_detail
from src.config import get_config
from src.get_args import get_args


def run():
    set_logging_config()
    logging.info(cfg['Info']['run'])
    print(cfg['Info']['run'])
    args = get_args()
    table = parse_table(args)
    works = parse_repo(args, table)
    students = get_students(works, args, table)
    write_rows(args, students)
    write_missing_studens_detail(args, students, table)
    if args['google_table']:
        os.remove(args['path'])


if __name__ == "__main__":
    cfg = get_config()
    try:
        run()
    except Exception as e:
        print(cfg['Error']['main'].format(e=e))
        exit(0)
