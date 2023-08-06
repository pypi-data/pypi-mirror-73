from scruf import compare


class Test:
    """
    A runable test

    Attributes
    ----------
    command : string
        The command the test is to compare against
    description : string
    output_specs : list of strings
         The expected result of the command
    """

    def __init__(self, command, setup_commands=None, description="", output_specs=None):
        self.command = command
        self.description = description
        self.output_specs = [] if output_specs is None else output_specs
        self.setup_commands = [] if setup_commands is None else setup_commands


class OutputSpec:
    """
    Specification of the expected output of a test

    Attributes
    ----------
    type: scruf.compare.ComparisonTypes
    content: str
        The expected output content
    source: str
        The expected source for the line, one of "stdout", "stderr", or
        "returncode"
    """

    def __init__(
        self, comp_type=compare.ComparisonTypes.BASIC, content="", source="stdout"
    ):
        self.comp_type = comp_type
        self.content = content
        self.source = source

    def compare(self, result_content):
        return compare.get_comparer(self.comp_type)(self.content, result_content)
