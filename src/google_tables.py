import urllib.request
import logging

GOOGLE_TABLE_NAME = "google_students_table_auto.csv"


def get_valid_link(link: str) -> str:
    return f"{link[:link.index('/edit')]}/export?format=csv&gid={link[link.index('gid=') + 4:]}"


def get_google_table(link: str, name: str = GOOGLE_TABLE_NAME) -> None:
    logging.info("Parse google table")
    try:
        urllib.request.urlretrieve(get_valid_link(link), name)
    except Exception as e:
        logging.error(f"Error work with google table: {e}")
        exit(0)

    return
