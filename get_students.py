from classes import Student


def get_students(works, args, table):
    students = []
    logins = []
    for row in table:
        login = row[args['github_col']-1]
        full_name = row[args['full_name_col'] - 1]
        group = row[args['group_col'] - 1]
        if login in logins:
            continue

        students.append(Student(full_name=full_name, group=group,
                                github=login, works=works[login]))

    return students
