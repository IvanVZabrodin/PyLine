from line import *
from os import system
system("title PyLine: Loading...")


class Terminal (Line):
    def __init__(self, name: str):
        self.name = name
