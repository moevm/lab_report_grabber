import logging
import os

from get_args import get_args
from parse_table import parse_table
from parse_github import parse_repo
from get_students import get_students
from fill_table import write_rows


def run():
    args = get_args()
    table = parse_table(args)
    works = parse_repo(args, table)
    students = get_students(works, args, table)
    write_rows(args, students)
    if args['google_table']:
        os.remove(args['path'])


if __name__ == "__main__":
    try:
        logging.info("Run")
        run()
    except Exception as e:
        print(f"Error in main file: {e}")
        exit(0)
