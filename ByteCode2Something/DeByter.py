from dataclasses import dataclass

import dis


@dataclass
class ByteCode:
    opcode: int
    arg: object
    color: str = "white"

    @property
    def opname(self) -> str:
        return dis.opname[self.opcode]

    def __str__(self):
        return f"{self.opname} {self.arg if self.opcode > dis.HAVE_ARGUMENT else ''}"

    def __post_init__(self):
        if self.opcode < dis.HAVE_ARGUMENT:
            self.arg = ""



class DeByter:
    def __init__(self, code):
        self.code = code
        self.bytes = iter(code.co_code)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            tmp = ByteCode(next(self.bytes), next(self.bytes))
            if tmp.opcode in dis.hasconst:
                tmp.arg = self.code.co_consts[tmp.arg]
                if isinstance(tmp.arg, str):
                    tmp.arg = f'"{tmp.arg}"'
                tmp.color = "red"
            elif tmp.opcode in dis.hasname:
                tmp.arg = self.code.co_names[tmp.arg]
                tmp.color = "blue"
            elif tmp.opcode in dis.haslocal:
                tmp.arg = self.code.co_varnames[tmp.arg]
                tmp.color = "green"
            elif tmp.opcode in dis.hascompare:
                tmp.arg = dis.cmp_op[tmp.arg]
                tmp.color = "yellow"
            elif tmp.opcode in dis.hasfree:
                tmp.arg = self.code.co_cellvars[tmp.arg]
                tmp.color = "magenta"
            return tmp
        except StopIteration:
            raise StopIteration
