from classes import Student
import logging
import log_config


def get_students(works, args, table):
    students = []
    for row in table:
        login = row[args['github_col'] - 1].lower()
        full_name = row[args['full_name_col'] - 1]
        group = row[args['group_col'] - 1]
        if login not in works.keys() or works[login] == []:
            continue

        logging.info(f"Add student: {login}, {full_name}, {group}")
        students.append(Student(full_name=full_name, group=group,
                                github=login, works=works[login]))

    return students
