from logging import Logger, Formatter, StreamHandler, INFO
from multiprocessing import get_logger
import sys


def create_logger() -> Logger:
    logger = get_logger()
    logger.setLevel(INFO)
    formatter = Formatter("%(asctime)s [%(levelname)s | %(processName)s] %(message)s")
    handler = StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    if not len(logger.handlers):
        logger.addHandler(handler)
    return logger
