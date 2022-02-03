from dataclasses import dataclass
from typing import Any
from types import CodeType
import dis


@dataclass
class l:
    value: int

class Compiler:
    def __init__(self, asm: str, filename = ""):
        self.asm = asm.strip()
        self.filename = filename


    def compile(self) -> CodeType:
        b = bytearray()
        consts = []
        names = []
        for line in self.asm.splitlines():
            x = line.strip().split(" ", 1)
            if len(x) > 1:
                arg = self.arg_parser(x[1])
            opname = x[0]
            opcode = dis.opmap[opname]
            b.append(opcode)
            
            if opcode < dis.HAVE_ARGUMENT:
                b.append(0)
            elif opcode in dis.hasconst:
                b.append(self.collection_adder(consts, arg))
            elif opcode in dis.hasname:
                b.append(self.collection_adder(names, arg))
            else:
                b.append(int(arg))

        return CodeType( 
            0,
            0,
            0,
            0,
            0,
            0,
            bytes(b),
            tuple(consts),
            tuple(names),
            (),
            self.filename,
            "",
            0,
            bytes(),
            (),
            (),
        )

    def collection_adder(self, collection, arg):
        if isinstance(arg, l):
            return arg.value
        elif arg in collection:
            return collection.index(arg)
        else:
            collection.append(arg)
            return len(collection) - 1

    def arg_parser(self, arg: str) -> Any:
        if arg.lower() == "None":
            return None
        elif arg[0] == "." or arg[0].isdigit():
            if "." in arg:
                return float(arg)
            else:
                return int(arg)
        elif arg.lower() == "true":
            return True
        elif arg.lower() == "false":
            return False
        elif arg.startswith(("'", '"')):
            return arg[1:-1]
        elif arg.startswith("$"):
            return l(int(arg[1:]))
        else:
            return arg