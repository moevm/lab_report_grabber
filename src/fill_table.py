import csv
import os
import logging
import log_config

def check_out_name(name):
    if name.endswith('.csv'):
        return name
    return name + '.csv'


def get_rows(students):
    rows = [['full_name', 'group', 'work_name', 'description', 'code']]
    for student in students:
        for work in student.get_fields():
            rows.append(work)
    return rows


def write_rows(args, students):
    rows = get_rows(students)
    name = check_out_name(args['out_table_name'])
    try:
        logging.info("Write out table")
        os.makedirs('out', exist_ok=True)
        with open(os.path.join('out', name), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    except Exception as e:
        print(f"Work with output file error: {e}")
        exit(0)
    return
