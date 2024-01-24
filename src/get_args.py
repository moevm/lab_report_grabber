import argparse
import csv
import logging
import log_config

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
                        type=str, help="Path to token file", required=True)
    parser.add_argument("--out_table_name", "-o",
                        type=str, help="Output table name", default='out')
    args = vars(parser.parse_args())

    logging.info("Parse works structure")
    try:
        with open(args['works_structure'], 'r') as f:
            rows = list(csv.reader(f))
    except Exception as e:
        print(f"Work with struct file error: {e}")
        exit(0)
    works_structure = {row[0]: [row[1], row[2]] for row in rows}
    args['works_structure'] = works_structure

    logging.info("Parse gh token")
    try:
        with open(args['token_file'], 'r') as f:
            row = f.readline()
    except Exception as e:
        print(f"Work with token file error: {e}")
        exit(0)

    token = row.replace('\n', '')
    args['token_file'] = token

    return args
