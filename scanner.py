from enum import Enum
from filter import Filter

keywords = ["start", "stop", "iter", "void", "int", "exit",
            "scanf", "printf", "main", "if", "then", "let", "data", "func"]

operators = ["=", "=>", "=<", "==", ":", "+", "-", "*",
             "/", "%", ".", "(", ")", ",", "{", "}", ";", "[", "]"]


class TokenID(Enum):
    IDENT_tk = 1
    NUM_tk = 2
    KW_tk = 3
    OP_tk = 4
    EOF_tk = 5


class Token:
    def __init__(self, id, instance, line):
        self.id = id
        self.instance = instance
        self.line = line


class Scanner:
    def __init__(self, fileName):
        self.Filter = Filter(fileName)

    def GetNextToken(self):
        (word, line) = self.Filter.GetNextString()
        if word == "EOF":
            return Token(TokenID.EOF_tk, word, line)
        if word in keywords:
            return Token(TokenID.KW_tk, word, line)
        elif word in operators:
            return Token(TokenID.OP_tk, word, line)
        elif word.isnumeric():
            return Token(TokenID.NUM_tk, word[0: 7], line)
        elif word[0].islower() and word.isalnum():
            return Token(TokenID.IDENT_tk, word[0: 7], line)
        else:
            raise Exception("Scanner Failed to read", word, line)
