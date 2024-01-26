from time import sleep
import collections
import logging

request_limit = 5000
log_counter = collections.Counter()


class CounterHandler(logging.Handler):
    def emit(self, record):
        log_counter[record.levelname] += 1
        if log_counter['DEBUG'] >= (request_limit - 100):
            print("The request limit has been exceeded. Pause for an hour")
            log_counter['DEBUG'] = 0
            sleep(60 * 60 + 5)  # 1 hour


class DebugFilter:
    def __call__(self, log):
        if log.levelno == logging.DEBUG:
            return True
        else:
            return False


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
