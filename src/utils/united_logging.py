import logging
import logging.handlers
import os

LOG_FNAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, 'log', 'MASTER.log')
LOG_NAME = 'UNITED'
LOG_LEVEL = logging.DEBUG


def get_united_logger():

    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(name)s] %(message)s')

    handler = logging.handlers.RotatingFileHandler(LOG_FNAME, maxBytes=1000, backupCount=5)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
