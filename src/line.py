from line_errors import OversizedMarkerError
from io import IOBase, open
from sys import stdout


class LineFormat:
    LEFT = -1
    MIDDLE = 0
    RIGHT = 1

    def __init__(self, mainchar: str = "-", endchar: str = "> ", linelen: int = 6, alignto: int = RIGHT):
        """
        mainchar: the line character of the input marker

        endchar: the end character of the input marker

        linelen: the length of the input marker
        """

        # invariants
        if len(mainchar) + len(endchar) > linelen:
            raise OversizedMarkerError(
                f"Unrepeated {mainchar} and {endchar} is over the maximum marker length {linelen}"
            )

        if not alignto in [LineFormat.LEFT, LineFormat.MIDDLE, LineFormat.RIGHT]:
            raise ValueError(f"Alignto value {alignto} does not correlate to LEFT, MIDDLE or RIGHT")

        self.mc = mainchar
        self.ec = endchar
        self.ll = linelen
        self.align = alignto

        # Calculated
        self.basic_out = self.mc * ((self.ll - len(self.ec)) // len(self.mc)) + self.ec

    def __len__(self) -> int:
        return self.ll

    def __mul__(self, text: str) -> str:
        out = list(self.basic_out)
        startpos = 0

        # Get aligned position

        if self.align != LineFormat.LEFT:
            startpos = self.ll - len(self.ec) - len(text)

            if self.align == LineFormat.MIDDLE:
                startpos //= 2

            if startpos < 0:
                startpos = 0

        for ind, i in enumerate(text):
            if startpos + ind >= self.ll - 2:
                out.insert(-len(self.ec), i)
            else:
                out[startpos + ind] = i

        return ''.join(out)


class Line:
    def __init__(self,
                 lform: LineFormat | tuple[str, str, int] | tuple[str, str, int, int],
                 stream: IOBase | str = stdout
                 ) -> None:
        """
        lform: The formating of the line marker
        stream: The io output to be written to. Default is stdout.
        """
        self.stream: IOBase = stream if issubclass(type(stream), IOBase) else open(stream, "a")
        self.line = lform if type(lform) == LineFormat else LineFormat(*lform)

    def display(self, message: str, premess: str = "") -> None:
        self.stream.write(self.line * premess + message + "\n")
