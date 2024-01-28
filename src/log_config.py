from time import sleep
import collections
import logging
import os

from src.config import get_config

cfg = get_config()

timeout = float(cfg['Const']['timeout'])
log_format = "%(asctime)s - %(levelname)s: %(message)s"
log_folder = cfg['Const']['log_folder']
logs_file = cfg['Const']['logs_file']
debug_file = cfg['Const']['debug_file']

log_counter = collections.Counter()


class DebugFilter:
    def __call__(self, log):
        return log.levelno == logging.DEBUG


class CounterHandler(logging.Handler):
    def emit(self, record):
        if record.levelname == 'DEBUG' and 'api.github.com' in record.getMessage():
            sleep(timeout)


def create_log_files() -> None:
    os.makedirs(log_folder, exist_ok=True)
    for file in [logs_file, debug_file]:
        file_path = os.path.join(log_folder, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass

    return


def set_logging_config() -> None:
    create_log_files()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(CounterHandler())
    logger.handlers[0].setLevel(logging.WARNING)

    handler = logging.FileHandler(os.path.join(log_folder, logs_file), "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.FileHandler(os.path.join(log_folder, debug_file), "w")
    handler.setLevel(logging.DEBUG)
    handler.addFilter(DebugFilter())
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return
