from scanner import Scanner, Token, TokenID
from myparser import Parser
from statSem import *
from compfs import *

parser = Parser("file")
tree = parser.GetTree()
parser.PrintTree(tree, 0)
stack = statSem(tree, Stack())
asm = ASM("file.asm",tree, stack.ids)
asm.run()
asm.file.close()
i = 1
