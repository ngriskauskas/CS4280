from scanner import Token, TokenID
from scanner import Scanner, Token, TokenID
from myparser import Parser
from statSem import *
import sys


class ASM:
    def __init__(self, outFile, root, ids):
        self.file = open(outFile,"w")
        self.labelNum = 0
        self.varNum = 0
        self.ids = ids
        self.root = root
    def getTemp(self):
        val = "T" + str(self.varNum)
        self.varNum += 1
        return val
    def getLabel(self):
        val = "L" + str(self.labelNum)
        self.labelNum +=1
        return val
    def run(self):
        self.convert(self.root)
        self.file.write("STOP" + "\n")
        for ident in self.ids:
            self.file.write(ident + " " + str(0) + "\n")
    def convert(self, root):
        if root.name == "out":
            self.convert(root.children[0])
            tempVar = self.getTemp()
            self.ids.append(tempVar)
            self.file.write("STORE " + tempVar + "\n")
            self.file.write("WRITE " + tempVar + "\n")
        elif root.name == "vars":
            if root.tokens is not None:
                self.file.write("LOAD " + str(root.tokens[3].instance) + "\n")
                self.file.write("STORE " + root.getIdToken().instance + "\n")
                if root.children[0] is not None:
                    self.convert(root.children[0])
        elif root.name == "in":
            idToken = root.getIdToken()
            self.file.write("READ " + idToken.instance+ "\n" )
        elif root.name == "R":
            tk = root.tokens[0]
            if tk.id in [TokenID.IDENT_tk, TokenID.NUM_tk] :
                self.file.write("LOAD " + tk.instance+ "\n")
            else:
                self.convert(root.children[0])
        elif root.name == "N":
            if root.tokens is None:
                self.convert(root.children[0])
            else:
                self.convert(root.children[1])
                tempVar = self.getTemp()
                self.ids.append(tempVar)
                self.file.write("STORE " + tempVar+ "\n")
                self.convert(root.children[0])
                if root.tokens[0].instance == "+":
                    self.file.write("ADD " + tempVar+ "\n")
                else:
                    self.file.write("SUB " + tempVar+ "\n")
        elif root.name == "expr":
            if root.tokens is None:
                self.convert(root.children[0])
            else:
                self.convert(root.children[1])
                tempVar = self.getTemp()
                ids.append(tempVar)
                self.file.write("STORE " + tempVar+ "\n")
                self.convert(root.children[0])
                if root.tokens[0].instance == "/":
                    self.file.write("DIV " + tempVar + "\n")
                else:
                    self.file.write("MULT " + tempVar+ "\n")
        elif root.name == "A":
            if root.tokens is not None and root.tokens[0] is not None:
                self.file.write("MULT " + str(-1))
            self.convert(root.children[0])
        elif root.name == "if":
            self.convert(root.children[2])
            tempVar = self.getTemp()
            self.ids.append(tempVar)
            self.file.write("STORE " + tempVar + "\n")
            self.convert(root.children[0])
            self.file.write("SUB " + tempVar + "\n")
            label = self.getLabel()
            r0 = root.children[1].tokens[0].instance
            if r0 == "=<":
                self.file.write("BRPOS " + label + "\n")
                self.convert(root.children[3])
            elif r0 == "=>":
                self.file.write("BRNEG " + label + "\n")
                self.convert(root.children[3])
            elif r0 == "==":
                self.file.write("BRNEG " + label + "\n")
                otherLabel = self.getLabel()
                self.file.write("BRPOS" + otherLabel+ "\n")
                self.convert(root.children[3])
                self.file.write(otherLabel + ": NOOP" + "\n")
            else:
                self.file.write("BRZERO " + label + "\n")
                self.convert(root.children[3])

            self.file.write(label + ": NOOP" + "\n")

        elif root.name == "loop":
            inlabel = self.getLabel()
            self.file.write(inlabel + ": NOOP" + "\n")
            self.convert(root.children[2])
            tempVar = self.getTemp()
            self.ids.append(tempVar)
            self.file.write("STORE " + tempVar + "\n")
            self.convert(root.children[0])
            self.file.write("SUB " + tempVar + "\n")
            r0 = root.children[1].tokens[0].instance
            outlabel = self.getLabel()
            if r0 == "=<":
                self.file.write("BRPOS " + outlabel + "\n")
                self.convert(root.children[3])
                self.file.write("BR " + inlabel + "\n")
            elif r0 == "=>":
                self.file.write("BRNEG " + outlabel + "\n")
                self.convert(root.children[3])
                self.file.write("BR " + inlabel + "\n")
            elif r0 == "==":
                self.file.write("BRNEG "+ outlabel + "\n")
                otherLabel = self.getLabel()
                self.file.write("BRPOS" + otherLabel+ "\n" )
                self.convert(root.children[3])
                self.file.write("BR ", inlabel)
                self.file.write(otherLabel + ": NOOP" + "\n")
            else:
                self.file.write("BRZERO " + outlabel + "\n")
                self.convert(root.children[3])
                self.file.write("BR ", inlabel)

            self.file.write(outlabel + ": NOOP" + "\n")
        elif root.name == "assign":
            self.convert(root.children[0])
            self.file.write("STORE " + root.tokens[0].instance + "\n")
        else:
            if root.children is not None:
                for child in root.children:
                    if child is not None:
                        self.convert(child)

