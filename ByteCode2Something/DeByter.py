from dataclasses import dataclass
from types import CodeType


import dis
from operator import ne


@dataclass
class ByteCode:
    opcode: int
    offset: int
    arg: object
    arg_resolved = ""
    color: str = "white"

    @property
    def opname(self) -> str:
        return dis.opname[self.opcode]

    def __str__(self):
        return f"{self.opname} {self.arg}"

    def __post_init__(self):
        if self.opcode < dis.HAVE_ARGUMENT:
            self.arg = ""



class DeByter:
    def __init__(self, code: CodeType):
        self.code = code
        self.bytes = iter(code.co_code)
        self.offset = 0

        return
            
    def __iter__(self):
        return self

    def __next__(self):
        try:
            tmp = ByteCode(next(self.bytes), self.offset, next(self.bytes))
            if tmp.opcode in dis.hasconst:
                tmp.arg_resolved = self.code.co_consts[tmp.arg]
                tmp.color = "red"
            elif tmp.opcode in dis.hasname:
                tmp.arg_resolved = self.code.co_names[tmp.arg]
                tmp.color = "blue"
            elif tmp.opcode in dis.haslocal:
                tmp.arg_resolved = self.code.co_varnames[tmp.arg]
                tmp.color = "green"
            elif tmp.opcode in dis.hascompare:
                tmp.arg_resolved = dis.cmp_op[tmp.arg]
                tmp.color = "yellow"
            elif tmp.opcode in dis.hasfree:
                tmp.arg_resolved = (self.code.co_cellvars + self.code.co_freevars)[tmp.arg]
                tmp.color = "magenta"
            elif tmp.opcode in dis.hasjrel: # Relative jump
                tmp.color = "dark_goldenrod" #ToDo
            elif tmp.opcode in dis.hasjabs: # Absolute jump
                tmp.color = "black"
            

            return tmp
        except StopIteration:
            raise StopIteration
