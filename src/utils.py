from github import Auth, Github
from typing import TextIO
import logging
import csv


def read_csv_table(f: TextIO) -> list[list[str]]:
    return list(csv.reader(f))


def read_token_file(f: TextIO) -> str:
    return f.readline()


def try_work_with_file(message: str, file: str, action, mode='r'):
    try:
        with open(file, mode) as f:
            answer = action(f)
    except Exception as e:
        logging.error(f"{message}: {e}")
        exit(0)

    return answer


def try_auth(message: str, token: str) -> Github:
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
    except Exception as e:
        logging.error(f"{message}: {e}")
        exit(0)

    return g


def get_work_names(args: dict, table: list[list[str]]):
    work_names = {}
    for row in table:
        name = row[args['eng_name_col'] - 1]
        surname = row[args['eng_surname_col'] - 1]
        login = row[args['github_col'] - 1].lower()
        for work in args['works_structure']:
            work_name = f"{surname}_{name}_{work}"
            work_names[work_name] = login

    return work_names
