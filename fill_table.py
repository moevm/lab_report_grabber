import csv
import os


def code_to_string(work):
    code = ""
    for file_name in work.code:
        code += f"{file_name}:\n\n{work.code[file_name]}\n\n"

    return code


def check_out_name(name):
    if name.endswith('.csv'):
        return name
    return name + '.csv'


def get_rows(students):
    rows = [['full_name', 'group', 'work_name', 'description', 'code']]
    for student in students:
        for work in student.works:
            code = code_to_string(work)
            rows.append([student.full_name, student.group, work.ru_name,
                         work.description, code])

    return rows


def write_rows(args, students):
    rows = get_rows(students)
    name = check_out_name(args['out_table_name'])
    with open(os.path.join('out', name), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return
