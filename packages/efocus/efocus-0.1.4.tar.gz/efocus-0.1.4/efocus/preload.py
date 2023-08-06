import sys
import re
import pathlib
import threading

from efocus import wrapper
from efocus.logging_filter import LoggingFilter
from efocus.logger import LOGGER


def should_filter_trace(frame):
    if frame.f_code.co_name.startswith("<"):
        return True

    try:
        trace_file_path = pathlib.Path(frame.f_code.co_filename)
    except TypeError:
        return True

    if pathlib.Path(".").absolute() not in trace_file_path.absolute().parents:
        return True

    for pattern in [
        "<frozen importlib._bootstrap_external>",
        "<frozen importlib._bootstrap>",
    ]:
        if pattern in frame.f_code.co_filename:
            return True

    return False


def run(function_pattern, log_enter):
    if log_enter:
        _trace_invocation(function_pattern)

    wrapper.wrap_logging((LoggingFilter(function_patterns=[function_pattern]),))


def _trace_invocation(function_pattern):
    def trace(frame, event, arg):
        if event == "call":
            if should_filter_trace(frame):
                return

            function_name = frame.f_code.co_name

            if re.match(function_pattern, function_name):
                parameter_message = (
                    f"with parameters {frame.f_locals}" if frame.f_locals else ""
                )

                LOGGER.info(f"{function_name} was called {parameter_message}")

    sys.settrace(trace)
    threading.settrace(trace)
