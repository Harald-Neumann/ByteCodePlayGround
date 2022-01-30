from opcode import opname
from types import CodeType
import dis

class Compiler:
    def __init__(self, asm: str, filename = ""):
        self.asm = asm.strip()
        self.filename = filename


    def compile(self) -> CodeType:
        b = bytearray()
        consts = []
        names = []
        for line in self.asm.splitlines():
            x = line.strip().split(" ")
            if len(x) == 2:
                arg = x[1]
            else:
                arg = ""
            opname = x[0]
            opcode = dis.opmap[opname]
            b.append(opcode)
            
            if opcode < dis.HAVE_ARGUMENT:
                b.append(0)
            elif opcode in dis.hasconst:
                if arg == "None":
                    consts.append(None)
                else:
                    consts.append(arg)
                b.append(len(consts) - 1)
            elif opcode in dis.hasname:
                names.append(arg)
                b.append(len(names) - 1)
            else:
                b.append(0)

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