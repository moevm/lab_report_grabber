import argparse
import logging

from src.utils import try_work_with_file, read_csv_table, read_token_file
from src.google_tables import get_google_table
from src.parse_table import find_col_for_name
from src.config import get_config

cfg = get_config()


def check_options(args: dict) -> None:
    fields = {
        'token': (args['token_file'], args['token']),
        'full_name': (args['full_name_col'], args['nfull_name_col']),
        'group': (args['group_col'], args['ngroup_col']),
        'github': (args['github_col'], args['ngroup_col'])
    }

    for field in fields:
        if not any(fields[field]):
            logging.error(cfg['Error']['empty_filed'].format(name=field))
            exit(0)

    return


def check_student_table(args: dict) -> None:
    default = cfg['Const']['google_table_name']
    if not args['google_table'] and args['path'] == default:
        logging.error(cfg['Error']['empty_table'])
        exit(0)

    return


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("--path", "-p",
                        type=str, default=cfg['Const']['google_table_name'],
                        help="Path to csv file")

    parser.add_argument("--google_table",
                        type=str, default=False,
                        help="Link to google table", )

    parser.add_argument("--num_header_rows",
                        type=int, default=1,
                        help="Num of header rows")

    parser.add_argument("--full_name_col",
                        type=int, default=False,
                        help="Full name column")

    parser.add_argument("--nfull_name_col",
                        type=str, default=False,
                        help="Named full name column")

    parser.add_argument("--group_col",
                        type=int, default=False,
                        help="Group column")

    parser.add_argument("--ngroup_col",
                        type=str, default=False,
                        help="Named group column")

    parser.add_argument("--github_col",
                        type=int, default=False,
                        help="Github column")

    parser.add_argument("--ngithub_col",
                        type=str, default=False,
                        help="Named github column")

    parser.add_argument("--works_structure", "-s",
                        type=str, required=True,
                        help='Path to works structure')

    parser.add_argument("--prefix",
                        type=str, required=True,
                        help="Prefix for repo")

    parser.add_argument("--token_file",
                        type=str, default=False,
                        help="Path to github token file")

    parser.add_argument("--token",
                        type=str, default=False,
                        help="Github token")

    parser.add_argument("--out_table_name", "-o",
                        type=str, default='out',
                        help="Output table name")

    return parser


def get_args() -> dict:
    parser = init_parser()
    args = vars(parser.parse_args())

    check_options(args)
    check_student_table(args)

    if args['google_table']:
        get_google_table(args['google_table'])
        args['path'] = cfg['Const']['google_table_name']

    named_cols = ['nfull_name_col', 'ngroup_col', 'ngithub_col']
    for named_col in named_cols:
        if args[named_col]:
            args[named_col[1:]] = find_col_for_name(args, args[named_col])

    logging.info(cfg['Info']['parse_token'])
    if args['token']:
        args['token_file'] = args['token']
    else:
        row = try_work_with_file(cfg['Error']['file'].format(name="token"),
                                 args['token_file'], read_token_file)
        token = row.replace('\n', '')
        args['token_file'] = token

    logging.info(cfg['Info']['parse_struct'])
    rows = try_work_with_file(cfg['Error']['file'].format(name="struct"),
                              args['works_structure'], read_csv_table)
    works_structure = {row[0]: [row[1], row[2]] for row in rows}
    args['works_structure'] = works_structure

    return args
