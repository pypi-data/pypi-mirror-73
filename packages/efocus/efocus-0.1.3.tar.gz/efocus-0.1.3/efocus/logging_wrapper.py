import builtins

import logging
import functools
from typing import Collection

from efocus.logging_filter import LoggingFilter


def wrap_log(log_func, logging_filters: Collection[LoggingFilter]):
    @functools.wraps(log_func)
    def wrapper(*args, **kwargs):
        for logging_filter in logging_filters:
            if logging_filter.should_filter(args, kwargs):
                return

        return log_func(*args, **kwargs)

    return wrapper


def wrap_next(next_function):
    @functools.wraps(next_function)
    def wrapper(*args, **kwargs):
        return next_function(*args, **kwargs)

    return wrapper


def wrap_range(range_func):
    @functools.wraps(range_func)
    def wrapper(*args, **kwargs):
        range_obj = range_func(*args, **kwargs)
        return range_obj

    return wrapper


def wrap_iteration():
    builtins.next = wrap_next(builtins.next)
    builtins.range = wrap_range(builtins.range)


def wrap_logging(logging_filters):
    builtins.print = wrap_log(builtins.print, logging_filters=logging_filters)
    logging.Logger._log = wrap_log(logging.Logger._log, logging_filters=logging_filters)
