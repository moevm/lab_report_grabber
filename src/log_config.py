import logging


class DebugFilter:
    def __call__(self, log):
        if log.levelno == logging.DEBUG:
            return True
        else:
            return False


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
