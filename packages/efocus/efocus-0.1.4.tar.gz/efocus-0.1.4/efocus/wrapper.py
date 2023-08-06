import builtins

import logging
import functools
from typing import Collection

from efocus.logging_filter import LoggingFilter
from efocus.logger import LOGGER


def wrap_log(log_func, logging_filters: Collection[LoggingFilter]):
    @functools.wraps(log_func)
    def wrapper(self, *args, **kwargs):
        if self != LOGGER:
            for logging_filter in logging_filters:
                if logging_filter.should_filter(args, kwargs):
                    return

        return log_func(self, *args, **kwargs)

    return wrapper


def wrap_print(print_func, logging_filters: Collection[LoggingFilter]):
    @functools.wraps(print_func)
    def wrapper(*args, **kwargs):
        for logging_filter in logging_filters:
            if logging_filter.should_filter(args, kwargs):
                return

        return print_func(*args, **kwargs)

    return wrapper


def wrap_logging(logging_filters):
    builtins.print = wrap_print(builtins.print, logging_filters=logging_filters)
    logging.Logger._log = wrap_log(logging.Logger._log, logging_filters=logging_filters)
