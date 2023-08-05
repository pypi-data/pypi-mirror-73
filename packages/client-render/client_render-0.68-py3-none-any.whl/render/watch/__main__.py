import logging
import time
from argparse import ArgumentParser

from render import LOG_DIR
from render.logger import configure_logger
from render.s3 import AWS_S3
from render.watch.logs import collect_instance_logs
from render.watch.screen import capture_screenshot
from render.watch.stat import log_usage, log_freq
from render.watch.window import WindowMgr

logger = logging.getLogger(__name__)


def main(args):
    s3 = AWS_S3()
    w = WindowMgr()

    log_freq()
    while True:
        w.find_window_wildcard(args.window_name)
        w.foreground()
        w.maximaze()

        capture_screenshot(s3)
        log_usage()

        collect_instance_logs(s3)

        logger.debug(f"Waiting {args.delay} seconds")
        time.sleep(args.delay)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("window_name")
    parser.add_argument("--delay", type=int, default=60)

    configure_logger(LOG_DIR / 'watch.log')
    try:
        main(parser.parse_args())
    except Exception as e:
        logger.exception(e)
        raise
