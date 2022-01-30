import marshal
from .Compiler import Compiler
from ByteCode2Something.DeByter import DeByter
from rich.console import Console

console = Console()

# code = """
#     LOAD_CONST 4
#     LOAD_NAME print
#     CALL_FUNCTION 0
#     POP_TOP
#     LOAD_CONST None
#     RETURN_VALUE
# """

code = """
    LOAD_CONST 4
    STORE_NAME a
    LOAD_CONST None
    RETURN_VALUE
"""

l = compile("print(4)", "<string>", "exec")
asm = Compiler(code, "test").compile()

def printByteCode(code, indent=0):
    console.print("-" * 50)
    console.print("\t"*indent, end = "")
    console.print(f"{code.co_name}")
    for i, bytecode in enumerate(DeByter(code)):
        console.print("\t"*indent, end = "")
        console.print(f"{i:03}|", style="grey74", end="")
        console.print(bytecode.opname, style=bytecode.color, end=" ")
        console.print(f"{bytecode.arg}" + ("" if bytecode.arg_resolved == "" else f" ({bytecode.arg_resolved})"))


print(len(asm.co_code))
exec(asm)

print(a)