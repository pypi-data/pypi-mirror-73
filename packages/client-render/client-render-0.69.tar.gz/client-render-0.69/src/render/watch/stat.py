import logging

import psutil
from s3transfer import MB

logger = logging.getLogger(__name__)


def log_freq():
    freq = psutil.cpu_freq()
    logger.info(f"CPU freq is {freq}")


def log_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    logger.info(f"CPU usage is {cpu_usage}")

    # windows is crashed on the getloadavg
    # load_average = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    # logger.info(f"Load average is {load_average}")

    memory = psutil.virtual_memory()
    used, total = round(memory.used / MB, 2), round(memory.total / MB, 2)
    logger.info(f"Memory usage is {used} MB - {total} MB")

    sw = psutil.swap_memory()
    logger.info(f"Swap usage is {sw.percent}%")
