import csv
import logging
import log_config
from github import Auth, Github


def read_csv_table(f):
    return list(csv.reader(f))


def read_token_file(f):
    return f.readline()


def try_work_with_file(message, file, action, mode='r'):
    try:
        with open(file, mode) as f:
            answer = action(f)
    except Exception as e:
        logging.error(f"{message}: {e}")
        exit(0)

    return answer


def try_auth(message, token):
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
    except Exception as e:
        logging.error(f"{message}: {e}")
        exit(0)

    return g
