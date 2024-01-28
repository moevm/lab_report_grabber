import configparser
import os


def get_config() -> dict:
    config = configparser.ConfigParser()
    config.read(os.path.join("src", "config.ini"))

    return config
