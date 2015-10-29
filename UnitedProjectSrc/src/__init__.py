# To make imports easier

from obj import flight
from input import read_in

import os
import logging
import logging.handlers

CURR_FILE_PATH = os.path.dirname(os.path.realpath('__file__'))

LOG_PATH = os.path.join(CURR_FILE_PATH, 'src', 'log', 'UNITED_MASTER.log')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

#Handler
my_handler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=1000, backupCount=5)

# Formatter
formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(name)s] %(message)s')

my_handler.setFormatter(formatter)

logger.addHandler(my_handler)
