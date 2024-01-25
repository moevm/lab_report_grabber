import logging
import os

from src.get_students import get_students
from src.parse_table import parse_table
from src.parse_github import parse_repo
from src.fill_table import write_rows
from src.get_args import get_args
import src.log_config


def run() -> None:
    args = get_args()
    table = parse_table(args)
    works = parse_repo(args, table)
    students = get_students(works, args, table)
    write_rows(args, students)
    if args['google_table']:
        os.remove(args['path'])

    return


if __name__ == "__main__":
    try:
        logging.info("Run")
        run()
    except Exception as e:
        print(f"Error in main file: {e}")
        exit(0)
