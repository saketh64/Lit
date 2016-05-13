import logging
from logging.handlers import RotatingFileHandler

def get_default_logging_handler():
    handler = RotatingFileHandler('out.log', maxBytes=1000000, backupCount=1)
    # create formatter
    formatter = logging.Formatter("%(name)s\t- %(levelname)s\t- %(message)s")
    # add formatter to handler
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler

################################
# Initialize Loggers for entire app
################################

logger_names = ["Lit","AM"]

for logger_name in logger_names:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = get_default_logging_handler()
    logger.addHandler(handler)