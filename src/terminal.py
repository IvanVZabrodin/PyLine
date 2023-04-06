from line import *
from QueriPlug.connections import *
from os import system

system("title PyLine: Loading...")


# TODO: Add documentation


class FunctionData:
    def __init__(self, name: str,
                 args: list[str | tuple[str, str | int | float | list | tuple | dict]],
                 code: str):
        self.args = args
        self.name = name
        self.code = code.replace("\n", "\n\t")
        self.lines = self.code.split("\n")

        self.func = f"""def {self.name}({','.join(self._parse_arglist())}):\n\t{self.code}"""

        self.functor = compile(self.func, "<string>", "exec")

    def _parse_arglist(self) -> list[str]:
        # TODO: Add param error checking
        arglist = []
        for arg in self.args:
            if type(arg) == str:
                arglist.append(arg)
            else:
                arglist.append(arg[0] + "=" + ("\"" + arg[1] + "\"" if type(arg[1]) == str else str(arg[1])))
        return arglist

    def __call__(self, args: str):
        exec(self.functor)
        return exec(self.name + "(" + args + ")")


class Terminal(Line):
    DATASTRUCTURE = [("TYPE", "CHAR(3) CHECK(TYPE IN ('var','func')) NOT NULL"),
                     ("NAME", "VARCHAR(25)"),
                     ("ARGS", "TINYTEXT"),
                     ("DEFAULTS", "TINYTEXT"),
                     ("VALUE", "TEXT")]

    def __init__(self, name: str, data_file: TableConnection | Connection,
                 lform: LineFormat | tuple[str, str, int] | tuple[str, str, int, int] = LineFormat()):
        super().__init__(lform)
        self.name = name

        self.vars = {}
        self.funcs = {}

        if type(data_file) == Connection:
            self.dtable = TableConnection(data_file, name, self.DATASTRUCTURE)
        else:
            self.dtable = data_file

        self._read_data()

    def _read_data(self, data=None):
        if data is None:
            data = self.dtable.getTable("*")

        for ditem in data:
            if ditem[1] == 'var':
                self.vars[ditem[2]] = ditem[5]
            else:
                args = ditem[3].split(',')
                defaults = ditem[4].split(',')
                self.funcs[ditem[2]] = FunctionData(ditem[2],
                                                    [i if defaults[ind] == "NO" else (i, defaults[ind])
                                                     for ind, i in enumerate(args)], ditem[5])

    def populateStd(self):
        pass

    def addItem(self):
        pass

    def __call__(self, expression: str) -> None:
        pass
