import logging

FOCUS_LOGGER_NAME = "eFocus"
LOGGER = logging.getLogger(FOCUS_LOGGER_NAME)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)
