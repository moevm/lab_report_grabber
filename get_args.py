from check_path import check_path
import argparse
import csv


def get_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("--path", "-p", type=str, help="Path to csv file")
    parser.add_argument("--num_header_rows", type=int, help="Num of header rows")
    parser.add_argument("--full_name_col", type=int, help="Full name column")
    parser.add_argument("--group_col", type=int, help="Group column")
    parser.add_argument("--github_col", type=int, help="Github column")
    parser.add_argument("--works_structure", "-s", type=str, help='Path to works structure and description')
    parser.add_argument("--prefix", type=str, help="Prefix for repo")
    parser.add_argument("--out_table_name", "-o", type=str, help="Output table name")
    args = vars(parser.parse_args())

    check_path(args['works_structure'])
    with open(args['works_structure'], 'r') as f:
        rows = list(csv.reader(f))
    works_structure = {row[0]: [row[1], row[2]] for row in rows}
    args['works_structure'] = works_structure

    return args
