"""Main entry point for CLI application"""
import argparse
import configparser
import re
import sys

import scruf
from scruf import compare, exception, execute, parse, run as scruf_run
from scruf.observers import tap


def run(argv):
    """Run scruf with options over some files

    Returns
    -------
    int
        0 if all tests pass, otherwise 1, suitable for sys.exit
    """
    options = _get_options(argv[1:])
    filenames = options.pop("files")
    try:
        _process_options(options)
    except OptionProcessingError as e:
        print("Failed to process options: {}".format(str(e)), file=sys.stderr)
        return 1

    observer = _build_observer()

    exit_code = 0 if run_files(filenames, options, observer) else 1
    return exit_code


def run_files(filenames, options, observer):
    success = True
    for filename in filenames:
        success &= run_file(filename, options, observer)
    return success


def run_file(filename, options, observer):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except (OSError, IOError) as file_error:
        observer.notify_file_open_error(filename, file_error)
        return False
    observer.notify_before_testing_file(filename)

    parser = parse.TestParser(options["indent"])
    try:
        tests = parser.parse(lines)
    except parse.ProgressionError as e:
        observer.notify_test_progression_error(filename, e)
        return False

    try:
        executor = execute.Executor(
            shell=options["shell"], cleanup=options["cleanup"], env=options["env"]
        )
    except execute.FailedToCreateTestDirError as e:
        observer.notify_execute_setup_error(filename, e)
        return False

    return run_tests(tests, executor, observer, options["strict"])


def run_tests(tests, executor, observer=None, strict=False):
    success = True
    observer.notify_before_tests_run(tests)

    for i, test in enumerate(tests):
        test_number = i + 1
        observer.notify_before_test_run(test, test_number)

        if not _run_setup_commands(test, test_number, executor, observer):
            success = False
            continue

        exec_result = executor.execute(test.command)
        try:
            compare_output = scruf_run.compare_result(test, exec_result)
        except (compare.RegexError, execute.OutOfLinesError) as e:
            observer.notify_test_error(test, test_number, e)
            success = False
            continue

        if strict:
            if not _check_for_strict_failure(test, test_number, exec_result, observer):
                success = False
                continue

        failure_summaries = [r for r in compare_output if not r["comparison_result"]]
        if len(failure_summaries) == 0:
            observer.notify_test_success(test, test_number)
        else:
            observer.notify_test_comparison_failure(
                test, test_number, failure_summaries
            )
            success = False
    return success


def _check_for_strict_failure(test, test_number, result, observer):
    strict_success = True
    observer_data = {}
    for source in ("stdout", "stderr"):
        if result.has_remaining_lines(source):
            observer_data[source] = result.get_remaining_lines(source)
            strict_success = False

    if not strict_success:
        observer.notify_test_strict_failure(test, test_number, observer_data)
    return strict_success


def _run_setup_commands(test, test_number, executor, observer):
    for setup_command in test.setup_commands:
        setup_result = executor.execute(setup_command)

        if setup_result.returncode != 0:
            observer.notify_setup_command_failure(
                test, test_number, setup_command, setup_result
            )
            return False
    return True


def _get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="FILE", nargs="+", help="File(s) to be tested")
    parser.add_argument(
        "--no-cleanup",
        action="store_false",
        dest="cleanup",
        help="Avoid cleaning up temporary test directory",
    )
    parser.add_argument(
        "-s",
        "--shell",
        type=str,
        help="Path to shell to be used to run tests with. Default is '/bin/sh'",
        default="/bin/sh",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=_indent_arg_type,
        default="    ",
        help="String to be used for detecting indentation when parsing tests. Default \
            is 4 spaces, use a literal '\\t' to denote a tab character",
    )
    parser.add_argument(
        "-e",
        "--env-file",
        type=str,
        help="Name of config file to read environment variables from",
    )
    parser.add_argument(
        "--version", action="version", version=str(scruf.__version__),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Whether tests should be run in strict mode. In this mode a test that \
            does not check each line of output is considered to have failed",
    )

    return vars(parser.parse_args(args))


def _process_options(options):
    if options["env_file"] is not None:
        env = _get_env_from_file(options["env_file"])
        options["env"] = env
    else:
        options["env"] = None
    options.pop("env_file")


def _indent_arg_type(string):
    # Convert literal "\t" to tab characters, e.g. for "--indent '\t'"
    string = re.sub(r"\\t", "\t", string)

    if not string.isspace():
        msg = "{} is not entirely whitespace".format(string)
        raise argparse.ArgumentTypeError(msg)
    return string


def _build_observer():
    # TODO: once more than one observer exists this should take an option to decide
    # which to use
    return tap.TapObserver()


def _get_env_from_file(filename):
    scruf_env_key = "Scruf Env"
    config = configparser.ConfigParser()
    # make config case-sensitive
    config.optionxform = str
    try:
        config.read(filename)
    except configparser.ParsingError as e:
        raise OptionProcessingError(
            "Unable to parse config file '{}': {}".format(filename, str(e)),
        )

    if scruf_env_key not in config:
        raise OptionProcessingError(
            "Could not find expected section: '{}' in config file: {}".format(
                scruf_env_key, filename
            ),
        )

    return config[scruf_env_key]


class OptionProcessingError(exception.CramerError):
    def __init__(self, msg=None):
        super().__init__(msg)
