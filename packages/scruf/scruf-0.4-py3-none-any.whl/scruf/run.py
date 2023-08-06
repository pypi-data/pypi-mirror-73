"""Test runner"""
from scruf import compare, parse


def compare_result(test, exec_result):
    """Compare a test's expected output against an execute result

    Parameters
    ----------
    test : scruf.test.Test
    exec_result : scruf.execute.Result

    Returns
    -------
    list of dict
        a list of the test result for each test line. Each dict contains keys:
            "result_line": str
                The line from the `exec_result` that was compared
            "result_source": str
                The source of the `"result_line"`, one of "stdout" or "stderr"
            "test_line": str
                The line from the `test` that was compared
            "comparison_result": bool
            "comparison_type": scruf.compare.ComparisonTypes
                The type of comparison made

    Raises
    ------
    scruf.compare.RegexError
        If the test contains a regex comparison with an invalid regex
    scruf.execute.OutOfLinesError
        If there are more lines in the test than the `exec_result`
    """
    summary = []

    for line in test.output_specs:
        output_spec = parse.OutputParser.parse(line)

        result_content = exec_result.get_content_for_comparison(
            output_spec.source, output_spec.comp_type
        )
        comparison = output_spec.compare(result_content)
        summary.append(
            {
                "result_line": result_content,
                "result_source": output_spec.source,
                "test_line": output_spec.content,
                "comparison_result": comparison,
                "comparison_type": output_spec.comp_type,
            }
        )
    return summary


def get_printable_failures(comparison):
    """Get a printable representation of a failed comparison

    Parameters
    ----------
    comparison : dict
        As returned `compare_result`

    Returns
    -------
    str
    """

    comparison_type = comparison["comparison_type"]

    return {
        compare.ComparisonTypes.BASIC: _basic_comparison_failure_lines,
        compare.ComparisonTypes.ESCAPE: _basic_comparison_failure_lines,
        compare.ComparisonTypes.NO_EOL: _no_eol_comparison_failure_lines,
        compare.ComparisonTypes.REGEX: _regex_comparison_failure_lines,
        compare.ComparisonTypes.RETURNCODE: _returncode_comparison_failure_lines,
    }[comparison_type](comparison["test_line"], comparison["result_line"])


def _format_content(content):
    formatted_content = repr(content)

    if not content.endswith("\n"):
        formatted_content += " (no eol)"
    return formatted_content


def _basic_comparison_failure_lines(comparison_content, result_content):
    return [
        "got: " + _format_content(result_content),
        "expected: " + _format_content(comparison_content),
    ]


def _no_eol_comparison_failure_lines(comparison_content, result_content):
    return _basic_comparison_failure_lines(
        comparison_content.rstrip("\r\n"), result_content
    )


def _regex_comparison_failure_lines(comparison_content, result_content):
    return [
        "got: " + _format_content(result_content),
        "Does not match: '{}'".format(comparison_content),
    ]


def _returncode_comparison_failure_lines(expected_returncode, got_returncode):
    return [
        "got return code: {} != {}".format(
            str(got_returncode), str(expected_returncode)
        )
    ]
