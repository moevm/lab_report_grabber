import logging
import json
import csv
import os

from src.classes import Student
from src.config import get_config

cfg = get_config()


def get_out_name(name: str) -> str:
    if name.endswith('.csv'):
        return name
    return name + '.csv'


def get_rows(students: list[Student]) -> list[list[str]]:
    rows = [json.loads(cfg['List']['out_header'])]
    for student in students:
        for work in student.get_fields():
            rows.append(work)
    return rows


def write_rows(args: dict, students: list[Student]) -> None:
    rows = get_rows(students)
    name = get_out_name(args['out_table_name'])
    try:
        logging.info(cfg['Info']['write_table'])
        os.makedirs('out', exist_ok=True)
        with open(os.path.join('out', name), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    except Exception as e:
        logging.error(cfg['Error']['output'].format(e=e))
        exit(0)
    return


def write_missing_studens_detail(args: dict, students: list[Student], table: list[list[str]]) -> None:
    missing = [["Группа", "ФИО", "GitHub", "lb№"]]
    for student in students:
        s_row = None
        for row in table:
            if row[args['github_col'] - 1].lower() == student.github:
                s_row = row
                break
        else:
            continue
        s_lbs = [work.eng_name[2:] for work in student.works]
        for i in args['lb_idxs']:
            if s_row[i - 1] != '' and str(i - args['lb_idxs'][0] + 1) not in s_lbs:
                missing.append([
                    student.group,
                    student.full_name, student.github, f"lb{i - args['lb_idxs'][0] + 1}"
                ])
    try:
        logging.info(cfg['Info']['write_table'])
        os.makedirs('out', exist_ok=True)
        with open(os.path.join('out', 'write_missing_studens_detail'), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(missing)
    except Exception as e:
        logging.error(cfg['Error']['output'].format(e=e))
        exit(0)
