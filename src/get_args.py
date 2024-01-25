import argparse
import logging
from utils import try_work_with_file, read_csv_table, read_token_file
from parse_table import find_col_for_name


def check_options(tokens, full_names, groups, githubs):
    if not any(tokens):
        logging.error("The token was not entered in any of the ways")
        exit(0)
    if not any(full_names):
        logging.error("The full name col was not entered in any of the ways")
        exit(0)
    if not any(groups):
        logging.error("The group col was not entered in any of the ways")
        exit(0)
    if not any(githubs):
        logging.error("The github col was not entered in any of the ways")
        exit(0)
    return


def get_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("--path", "-p",
                        type=str, help="Path to csv file", required=True)
    parser.add_argument("--num_header_rows",
                        type=int, help="Num of header rows", default=1)
    parser.add_argument("--full_name_col",
                        type=int, help="Full name column", required=False)
    parser.add_argument("--nfull_name_col",
                        type=str, help="Named full name column", required=False)
    parser.add_argument("--group_col",
                        type=int, help="Group column", required=False)
    parser.add_argument("--ngroup_col",
                        type=str, help="Named group column", required=False)
    parser.add_argument("--github_col",
                        type=int, help="Github column", required=False)
    parser.add_argument("--ngithub_col",
                        type=str, help="Named github column", required=False)
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

    check_options((args['token_file'], args['token']),
                  (args['full_name_col'], args['nfull_name_col']),
                  (args['group_col'], args['ngroup_col']),
                  (args['github_col'], args['ngroup_col']))

    named_cols = ['nfull_name_col', 'ngroup_col', 'ngithub_col']
    for named_col in named_cols:
        if args[named_col]:
            args[named_col[1:]] = find_col_for_name(args, args[named_col])

    logging.info("Parse gh token")
    if args['token']:
        args['token_file'] = args['token']
    else:
        row = try_work_with_file("Work with token file error", args['token_file'], read_token_file)
        token = row.replace('\n', '')
        args['token_file'] = token

    logging.info("Parse works structure")
    rows = try_work_with_file("Work with struct file error", args['works_structure'], read_csv_table)
    works_structure = {row[0]: [row[1], row[2]] for row in rows}
    args['works_structure'] = works_structure

    return args
