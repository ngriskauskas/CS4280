from scanner import Scanner, Token, TokenID
from myparser import Parser
from statSem import *

parser = Parser("file")
tree = parser.GetTree()
parser.PrintTree(tree, 0)
stack = statSem(tree, Stack())

i = 1
