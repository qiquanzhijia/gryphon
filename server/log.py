import logging
import logging.handlers
import sys


class LoggerWriter:
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != '\n':
            self.level(message)

    def flush(self):
        pass


def setup():
    log_file = 'app.log'

    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s ' \
          '%(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    ch = logging.StreamHandler()
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)

    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if True:
        logger.addHandler(ch)
    else:
        sys.stdout = LoggerWriter(logger.debug)
        sys.stderr = LoggerWriter(logger.warning)


def get_logger():
    return logging.getLogger("app")
