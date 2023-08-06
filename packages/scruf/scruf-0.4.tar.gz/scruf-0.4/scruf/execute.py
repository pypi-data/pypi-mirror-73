import os
import shutil
import subprocess
import tempfile

from scruf import compare, exception


class Executor:
    """
    Class for executing commands

    Attributes
    ----------
    shell : str
        The shell to be used to run the command
    cleanup : bool
        Weather or not to remove created temporary directories once a command is run
    path : str
        Path to use in the 'TESTDIR' environment variable when executing commands
    tmpdir : str
        Directory under which the testdir will be created for running commands
    env : dict
        Environment to be used when running the command, defaults to `os.environ`

    Raises
    ------
    scruf.execute.FailedToCreateTestDirError
        If unable to create a directory under `tmpdir`. Specifically, if attempting to
        create this directory raises `PermissionError`or `FileNotFoundError`
    """

    def __init__(
        self, shell="/bin/sh", cleanup=True, path=os.getcwd(), tmpdir="/tmp", env=None,
    ):
        self.cleanup = cleanup
        self.shell = shell
        self.env = self._setup_env(env, path)

        # Might raise exception, so set this last
        self.testdir = self._mktestdir(tmpdir)

    def execute(self, command):
        """Execute a command

        Parameters
        ----------
        command : str


        Returns
        -------
        tuple
            int : The return code from executing the command
            string : The stdout generated from the command
            string : The stderr generated from the command
        """

        p = subprocess.Popen(
            [self.shell, "-"],
            cwd=self.testdir,
            env=self.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        stdout, stderr = p.communicate(command)

        return Result(p.returncode, stdout, stderr)

    def __del__(self):
        if self.cleanup and hasattr(self, "testdir"):
            shutil.rmtree(self.testdir)

    @staticmethod
    def _setup_env(env, path):
        if env is None:
            env = os.environ
        _maybe_add_to_env(env, "TESTDIR", path)
        return env

    @staticmethod
    def _mktestdir(tmpdir):
        try:
            testdir = tempfile.mkdtemp(dir=tmpdir, suffix="scruf")
        except (PermissionError, FileNotFoundError) as e:
            raise FailedToCreateTestDirError(tmpdir, e)
        return testdir


class Result:
    """
    Represents the result of executing a command

    Attributes
    ----------
    returncode : int
    stdout : str
    stderr : str
    """

    def __init__(self, returncode, stdout="", stderr=""):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

        self._stdout_index = 0
        self._stdout_lines = stdout.splitlines(True)

        self._stderr_index = 0
        self._stderr_lines = stderr.splitlines(True)

    """Get the next line from the given source

    Parameters
    ----------
    source : { "stdout", "stderr" }
        The source to extra the next line from

    Returns
    -------
    str
        The next line from the source

    Raises
    ------
    scruf.execute.OutOfLinesError
        If there are no more lines available for the given source
    """

    def next_line(self, source):
        index_attr = self._index_for_source(source)
        index = getattr(self, index_attr)
        lines = getattr(self, self._lines_for_source(source))

        if index == len(lines):
            raise OutOfLinesError(self, source)
        else:
            setattr(self, index_attr, index + 1)
            line = lines[index]
            return line

    def has_remaining_lines(self, source):
        lines = getattr(self, self._lines_for_source(source))
        index = getattr(self, self._index_for_source(source))
        return index <= len(lines) - 1

    def get_remaining_lines(self, source):
        lines = getattr(self, self._lines_for_source(source))
        index = getattr(self, self._index_for_source(source))
        return lines[index:]

    def get_content_for_comparison(self, source, comp_type):
        if comp_type == compare.ComparisonTypes.RETURNCODE:
            return self.returncode
        return self.next_line(source)

    @staticmethod
    def _index_for_source(source):
        return "_" + source + "_index"

    @staticmethod
    def _lines_for_source(source):
        return "_" + source + "_lines"


class OutOfLinesError(exception.CramerError):
    def __init__(self, result, source):
        message = "No more lines available for {}:\n".format(source)
        message += "\t" + self._build_stream_content_msg(result, "stdout")
        message += "\t" + self._build_stream_content_msg(result, "stderr")
        super().__init__(message)

        self.result = result
        self.source = source

    @staticmethod
    def _build_stream_content_msg(result, stream):
        content = getattr(result, stream)
        msg = "{} was: ".format(stream)
        if content:
            return msg + content
        return msg + "(no content)\n"


class FailedToCreateTestDirError(exception.CramerError):
    def __init__(self, dir_name, file_error):
        message = "Could not create temporary directory at {}: {}".format(
            dir_name, str(file_error)
        )
        super().__init__(message)

        self.dir_name = dir_name


def _maybe_add_to_env(env, name, value):
    if name not in env:
        env[name] = value
