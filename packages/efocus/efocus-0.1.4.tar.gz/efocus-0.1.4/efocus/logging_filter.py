from typing import List
import traceback
import re

from efocus.error import EloggingError


class InvalidRegexPattern(EloggingError):
    def __init__(self, function_pattern):
        super().__init__(
            f"The pattern '{function_pattern}' is not a valid regex pattern."
        )


class LoggingFilter:
    def __init__(self, function_patterns: List[str]):
        for function_pattern in function_patterns:
            if not self._is_valid_pattern(function_pattern):
                raise InvalidRegexPattern(function_pattern)

        self.function_pattern = function_patterns

    def should_filter(self, args, kwargs) -> bool:
        stack = [item.name for item in traceback.extract_stack()]
        for function_pattern in self.function_pattern:
            for stack_item in stack:
                if re.match(function_pattern, stack_item):
                    return False

        return True

    @staticmethod
    def _is_valid_pattern(pattern):
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
