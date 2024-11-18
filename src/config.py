import configparser
import os


def get_config() -> dict:
    config = configparser.ConfigParser()
    config.read(os.path.join("", "config.ini"))

    return config
