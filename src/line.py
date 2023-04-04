from line_errors import OversizedMarkerError
from io import open, UnsupportedOperation, IOBase
from sys import stdout, stdin


class LineFormat:
    LEFT = -1
    MIDDLE = 0
    RIGHT = 1

    def __init__(self, mainchar: str = "-", endchar: str = "> ", linelen: int = 7, alignto: int = RIGHT) -> None:
        """
        :param mainchar: The line character of the line marker.
        :param endchar: The end character of the line marker.
        :param linelen: The length of the line marker.
        :param alignto: The alignment of text that is displayed inside the line marker.

        Alignment:
        =========

        Alignment is used for text that is displayed inside the line marker.
        There are three alignments:
        ::
            LineFormat.LEFT
            LineFormat.MIDDLE
            LineFormat.RIGHT

        The rules for these are as follows:

        ========= ======= ========
        Alignment Message Result
        ========= ======= ========
        LEFT      'int'   'int---> '

        MIDDLE    'int'   '-int-> '

        RIGHT     'int'   '---int> '
        ========= ======= ========

        If the desired text is larger than the length of the Line, the Line will extend to fit, always keeping the end
        character - in this case '> '.
        """

        # invariants
        if len(mainchar) + len(endchar) > linelen:
            raise OversizedMarkerError(
                f"Unrepeated {mainchar} and {endchar} is over the maximum marker length {linelen}"
            )

        if alignto not in [LineFormat.LEFT, LineFormat.MIDDLE, LineFormat.RIGHT]:
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
                 stream: IOBase | tuple[IOBase, IOBase] | str = tuple([stdin, stdout])
                 ) -> None:
        """
        :param lform: The formating of the line marker.
        :param stream: The io output to be written to. Default is stdout (Terminal/Command Line). Can also be two
         seperate objects for reading and writting.
        :return:
        """
        if type(stream) == tuple:
            self.streamin = stream[0]
            self.streamout = stream[1]
        elif type(stream) == str:
            self.streamin = open(stream, "a")
            self.streamout = self.streamin
        else:
            self.streamin = stream
            self.streamout = stream

        if not self.streamin.readable() or not self.streamout.writable():
            raise UnsupportedOperation("Line stream not readable and writtable")

        self.line = lform if type(lform) == LineFormat else LineFormat(*lform)

    def display(self, message: str, linemess: str = "", end: str = "\n") -> None:
        """
        :param message: The main message displayed after the line marker.
        :param linemess: The message displayed inside the line marker.
        :param end: The ending character after displaying. Default is endline.
        :return:
        """
        self.streamout.write(self.line * linemess + message + end)

    def request(self, linemess: str = "") -> str:
        """
        :param linemess: The message displayed inside the line marker.
        :return: The result from the request.
        """
        self.streamout.write(self.line * linemess)
        return str(self.streamin.readline())
