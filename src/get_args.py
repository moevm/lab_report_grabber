import argparse
import logging
from utils import try_work_with_file, read_csv_table, read_token_file


def get_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("--path", "-p",
                        type=str, help="Path to csv file", required=True)
    parser.add_argument("--num_header_rows",
                        type=int, help="Num of header rows", default=1)
    parser.add_argument("--full_name_col",
                        type=int, help="Full name column", required=True)
    parser.add_argument("--group_col",
                        type=int, help="Group column", required=True)
    parser.add_argument("--github_col",
                        type=int, help="Github column", required=True)
    parser.add_argument("--works_structure", "-s",
                        type=str, help='Path to works structure', required=True)
    parser.add_argument("--prefix",
                        type=str, help="Prefix for repo", required=True)
    parser.add_argument("--token_file",
                        type=str, help="Path to token file", default=False)
    parser.add_argument("--token",
                        type=str, help="Path to token file", default=False)
    parser.add_argument("--out_table_name", "-o",
                        type=str, help="Output table name", default='out')
    args = vars(parser.parse_args())
    if not args['token_file'] and not args['token']:
        logging.error("The token was not entered in any of the ways")
        exit(0)

    logging.info("Parse gh token")
    if args['token_file']:
        row = try_work_with_file("Work with token file error", args['token_file'], read_token_file)
        token = row.replace('\n', '')
        args['token_file'] = token
    else:
        args['token_file'] = args['token']

    logging.info("Parse works structure")
    rows = try_work_with_file("Work with struct file error", args['works_structure'], read_csv_table)
    works_structure = {row[0]: [row[1], row[2]] for row in rows}
    args['works_structure'] = works_structure

    return args
