import logging
import logging.config

import pathlib
import os

current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)

dir_ = os.path.join(current_dir, "logging.conf")
if os.path.exists(dir_) == True:
    logging.config.fileConfig(dir_, disable_existing_loggers=False)
else:
    raise Exception('no log')
# create logger
logger = logging.getLogger('simpleExample')
