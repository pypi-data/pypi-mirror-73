"""Comparison logic for tests"""
import enum
import re

from scruf import exception

_EOL_CHARACTERS = "\n\r"


class ComparisonTypes(enum.Enum):
    """The possible types of comparison"""

    BASIC = enum.auto()
    ESCAPE = enum.auto()
    REGEX = enum.auto()
    NO_EOL = enum.auto()
    RETURNCODE = enum.auto()


def get_comparer(comparison_type):
    """Get function to be used to make comparison for the given type

    Note if `comparison_type` is `scruf.compare.ComparisonTypes.REGEX`, the returned
    function will raise a `scruf.compare.RegexError` if it is run with an invalid regex.

    Parameters
    ----------
    comparison_type : scruf.compare.ComparisonTypes

    Returns
    -------
    function(expected_content, exec_result_content)
        Function that can be used to make the comparison, returning bool
    """
    return {
        ComparisonTypes.BASIC: _basic_compare,
        ComparisonTypes.ESCAPE: _basic_compare,
        ComparisonTypes.REGEX: _regex_compare,
        ComparisonTypes.NO_EOL: _no_eol_compare,
        ComparisonTypes.RETURNCODE: _returncode_compare,
    }[comparison_type]


class RegexError(exception.CramerError):
    def __init__(self, regex, regex_error):
        message = "Error in regex {}: {}".format(regex, str(regex_error))
        super().__init__(message)

        self.regex = regex


def _basic_compare(expected_content, content):
    return content == expected_content


def _returncode_compare(expected_returncode, returncode):
    return returncode == expected_returncode


def _no_eol_compare(expected_content, content):
    return _basic_compare(expected_content.rstrip(_EOL_CHARACTERS), content)


def _build_regex(test_line):
    try:
        regex = re.compile(test_line)
    except re.error as e:
        raise RegexError(test_line, e)
    return regex


def _regex_compare(raw_regex, content):
    regex = _build_regex(raw_regex)
    return regex.search(content) is not None
