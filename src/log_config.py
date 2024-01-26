from time import sleep
import collections
import logging

from src.requests_limit import check_requests_limit

timeout = 1  # secs
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


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(CounterHandler())

handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler("logs/logs.log", "w")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler("logs/debug.log", "w")
handler.setLevel(logging.DEBUG)
handler.addFilter(DebugFilter())
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
