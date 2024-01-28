import urllib.request
import logging

from src.config import get_config

cfg = get_config()


def get_valid_link(link: str) -> str:
    return f"{link[:link.index('/edit')]}/export?format=csv&gid={link[link.index('gid=') + 4:]}"


def get_google_table(link: str) -> None:
    logging.info(cfg['Info']['parse_table'].format(where='google table'))
    try:
        urllib.request.urlretrieve(get_valid_link(link), cfg['Const']['google_table_name'])
    except Exception as e:
        logging.error(cfg['Error']['google_table'.format(e=e)])
        exit(0)

    return
