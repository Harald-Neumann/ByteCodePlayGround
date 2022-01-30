from ByteCode2Something.DeByter import DeByter
from rich.console import Console

console = Console()

code = compile("""
a = 5
b = 'text'
def f(x):
    def g(y):
        return x + y
    return x + 1
f(5)
def LoL():
    pass
if a > 12:
    print(b)
else:
    print(a)

""", "<string>", "exec")



def printByteCode(code, indent=0):
    console.print("-" * 50)
    console.print("\t"*indent, end = "")
    console.print(f"{code.co_name}")
    for i, bytecode in enumerate(DeByter(code)):
        console.print("\t"*indent, end = "")
        console.print(f"{i:03}|", style="grey74", end="")
        console.print(bytecode.opname, style=bytecode.color, end=" ")
        console.print(bytecode.arg)
    

def doCode(code, indent=0):
    printByteCode(code, indent)
    for i in code.co_consts:
        if hasattr(i, "co_code"):
            doCode(i, indent + 1)

doCode(code)
