#!/usr/bin/python
from scanner import Token, TokenID
from scanner import Scanner, Token, TokenID
from myparser import Parser
from statSem import *
from conv import *
import sys

filename = str(sys.argv[1])        
parser = Parser(filename)
tree = parser.GetTree()
parser.PrintTree(tree, 0)
stack = statSem(tree, Stack())

asm = ASM(filename + ".asm",tree, stack.ids)
asm.run()
asm.file.close()
print(filename + ".asm")
