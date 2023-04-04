from line import *
from os import system
system("title PyLine: Loading...")


class Terminal (Line):
    def __init__(self, name: str, lform: LineFormat | tuple[str, str, int] | tuple[str, str, int, int] = LineFormat()):
        super(lform)
        self.name = name

