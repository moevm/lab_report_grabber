import argparse
import ast


def get_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("--path", "-p", type=str, help="Path to csv file")
    parser.add_argument("--num_header_rows", type=int, help="Num of header rows")
    parser.add_argument("--full_name_col", type=int, help="Full name column")
    parser.add_argument("--group_col", type=int, help="Group column")
    parser.add_argument("--github_col", type=int, help="Github column")
    parser.add_argument("--works_structure", "-s", type=lambda x: ast.literal_eval(x), help='Works structure')
    parser.add_argument("--prefix", type=str, help="Prefix for repo")
    parser.add_argument("--out_table_name", "-o", type=str, help="Output table name")
    args = parser.parse_args()

    return vars(args)
