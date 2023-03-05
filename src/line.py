from io import IOBase
from sys import stdout


class Line:
    def __init__(self, stream: IOBase = stdout) -> None:
        """
        stream: The io output to be written to. Default is stdout.
        """

        self.stream: IOBase = stream



Line()