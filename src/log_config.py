from time import sleep
import collections
import logging
import os

# from src.requests_limit import check_requests_limit

timeout = 1  # secs
log_folder = 'log'
logs_file = 'logs.log'
debug_file = 'debug.log'
log_counter = collections.Counter()


class DebugFilter:
    def __call__(self, log):
        return log.levelno == logging.DEBUG


class CounterHandler(logging.Handler):
    def emit(self, record):
        log_counter[record.levelname] += 1
        if record.levelname == 'DEBUG':
            # log_counter['DEBUG'] = check_requests_limit(log_counter['DEBUG'])
            sleep(timeout)


def create_log_files() -> None:
    os.makedirs('log', exist_ok=True)
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
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.FileHandler(os.path.join(log_folder, debug_file), "w")
    handler.setLevel(logging.DEBUG)
    handler.addFilter(DebugFilter())
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return
