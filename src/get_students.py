import logging

from src.config import get_config
from src.classes import Student

cfg = get_config()


def get_students(works: dict, args: dict, table: list[list[str]]) -> list[Student]:
    students = []
    for row in table:
        login = row[args['github_col'] - 1].lower()
        full_name = row[args['full_name_col'] - 1]
        group = row[args['group_col'] - 1]
        if login not in works.keys() or works[login] == []:
            continue

        logging.info(cfg['Info']['add_student'].format(full_name=full_name,
                                                       login=login, group=group))
        students.append(Student(full_name=full_name, group=group,
                                github=login, works=works[login]))

    return students
