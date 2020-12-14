from scanner import Scanner, TokenID, Token
# create parse tree
# func for printing parse tree preorder tranversal with indent 2 spaces

# parser auxiliary func from notes
# func for each nonterminal in grammar named as nonterminal


class Node:
    def __init__(self, name, children, tokens):
        self.name = name
        self.children = children
        self.tokens = tokens

    def getIdToken(self):
        if self.tokens is not None:
            for token in self.tokens:
                if token.id == TokenID.IDENT_tk:
                    return token


class Parser:
    def __init__(self, fileName):
        self.scanner = Scanner(fileName)
        self.tk = self.scanner.GetNextToken()

    def GetTree(self):
        return self.program()

    def program(self):
        (tok1, cons) = self.TryConsume("start")
        if cons:
            vars = self.vars()
            (tok2, cons) = self.TryConsume("main")
            if cons:
                block = self.block()
                (tok3, cons) = self.TryConsume("stop")
                if cons:
                    return Node("program", [vars, block], [tok1, tok2, tok3])
        self.error()

    def block(self):
        (tok1, cons) = self.TryConsume("{")
        if cons:
            vars = self.vars()
            stats = self.stats()
            (tok2, cons) = self.TryConsume("}")
            if cons:
                return Node("block", [vars, stats], [tok1, tok2])

        self.error()

    def vars(self):
        (tok1, cons) = self.TryConsume("let")
        if cons:
            if self.tk.id == TokenID.IDENT_tk:
                tok2 = self.tk
                self.tk = self.scanner.GetNextToken()
                (tok3, cons) = self.TryConsume(":")
                if cons:
                    if self.tk.id == TokenID.NUM_tk:
                        tok4 = self.tk
                        self.tk = self.scanner.GetNextToken()
                        vars = self.vars()
                        return Node("vars", [vars], [tok1, tok2, tok3, tok4])
                else:
                    self.error()
            else:
                self.error()
        return

    def expr(self):
        N = self.N()
        (tk, cons) = self.TryConsume(["/", "*"])
        if cons:
            expr = self.expr()
            return Node("expr", [N, expr], [tk])
        return Node("expr", [N], None)

    def N(self):
        A = self.A()
        (tk, cons) = self.TryConsume(["+", "-"])
        if cons:
            N = self.N()
            return Node("N", [A, N], [tk])
        return Node("N", [A], None)

    def A(self):
        (tk, cons) = self.TryConsume("%")
        if cons:
            A = self.A()
            return Node("A", [A], [tk])
        else:
            R = self.R()
            return Node("A", [R], None)

    def R(self):
        (tok1, cons) = self.TryConsume("[")
        if cons:
            expr = self.expr()
            (tok2, cons) = self.TryConsume("]")
            if cons:
                return Node("R", [expr], [tok1, tok2])
        elif self.tk.id == TokenID.IDENT_tk:
            tk = self.tk
            self.tk = self.scanner.GetNextToken()
            return Node("R", None, [tk])
        elif self.tk.id == TokenID.NUM_tk:
            tk = self.tk
            self.tk = self.scanner.GetNextToken()
            return Node("R", None, [tk])
        self.error()

    def stats(self):
        stat = self.stat()
        mstat = self.mstat()
        return Node("stats", [stat, mstat], None)

    def mstat(self):
        if self.tk.instance in ["scanf", "printf", "{", "if", "iter"]:
            stat = self.stat()
            mstat = self.mstat()
            return Node("mstat", [stat, mstat], None)
        elif self.tk.id == TokenID.IDENT_tk:
            stat = self.stat()
            mstat = self.mstat()
            return Node("mstat", [stat, mstat], None)
        return Node("mstat", None, None)

    def stat(self):
        if self.tk.instance == "scanf":
            inn = self.inn()
            (tok, cons) = self.TryConsume(".")
            if cons:
                return Node("stat", [inn], [tok])
        elif self.tk.instance == "printf":
            out = self.out()
            (tok, cons) = self.TryConsume(".")
            if cons:
                return Node("stat", [out], [tok])
        elif self.tk.instance == "{":
            block = self.block()
            return Node("stat", [block], None)
        elif self.tk.instance == "if":
            iff = self.iff()
            (tok, cons) = self.TryConsume(".")
            if cons:
                return Node("stat", [iff], [tok])
        elif self.tk.instance == "iter":
            loop = self.loop()
            (tok, cons) = self.TryConsume(".")
            if cons:
                return Node("stat", [loop], [tok])
        elif self.tk.id == TokenID.IDENT_tk:
            assign = self.assign()
            (tok, cons) = self.TryConsume(".")
            if cons:
                return Node("stat", [assign], [tok])
        self.error()

    def inn(self):
        (tok1, cons) = self.TryConsume("scanf")
        if cons:
            (tok2, cons) = self.TryConsume("[")
            if cons:
                if self.tk.id == TokenID.IDENT_tk:
                    tok3 = self.tk
                    self.tk = self.scanner.GetNextToken()
                    (tok4, cons) = self.TryConsume("]")
                    if cons:
                        return Node("in", None, [tok1, tok2, tok3, tok4])
        self.error()

    def out(self):
        (tok1, cons) = self.TryConsume("printf")
        if cons:
            (tok2, cons) = self.TryConsume("[")
            if cons:
                expr = self.expr()
                (tok3, cons) = self.TryConsume("]")
                if cons:
                    return Node("out", [expr], [tok1, tok2, tok3])
        self.error()

    def iff(self):
        (tok1, cons) = self.TryConsume("if")
        if cons:
            (tok2, cons) = self.TryConsume("[")
            if cons:
                expr1 = self.expr()
                R0 = self.RO()
                expr2 = self.expr()
                (tok3, cons) = self.TryConsume("]")
                if cons:
                    (tok4, cons) = self.TryConsume("then")
                    if cons:
                        block = self.block()
                        return Node("if", [expr1, R0, expr2, block], [tok1, tok2, tok3, tok4])
        self.error()

    def loop(self):
        (tok1, cons) = self.TryConsume("iter")
        if cons:
            (tok2, cons) = self.TryConsume("[")
            if cons:
                expr1 = self.expr()
                R0 = self.RO()
                expr2 = self.expr()
                (tok3, cons) = self.TryConsume("]")
                if cons:
                    block = self.block()
                    return Node("loop", [expr1, R0, expr2, block], [tok1, tok2, tok3])
        self.error()

    def assign(self):
        if self.tk.id == TokenID.IDENT_tk:
            tok1 = self.tk
            self.tk = self.scanner.GetNextToken()
            (tok2, cons) = self.TryConsume("=")
            if cons:
                expr = self.expr()
                return Node("assign", [expr], [tok1, tok2])
        self.error()

    def RO(self):
        (tok1, cons) = self.TryConsume(["=<", "=>", "=="])
        if cons:
            return Node("RO", None, [tok1])
        (tok2, cons) = self.TryConsume(":")
        if cons:
            (tok3, cons) = self.TryConsume(":")
            if cons:
                return Node("RO", None, [tok2, tok3])
        self.error()

    def error(self):
        raise Exception("Failed to parse", self.tk.instance, self.tk.line)

    def TryConsume(self, vals):
        tk = self.tk
        if self.tk.instance in vals:
            self.tk = self.scanner.GetNextToken()
            return (tk, True)
        return (tk, False)

    def PrintTree(self, root, level):
        print("=======================")
        print(' ' * level, "Label: ", root.name)
        if root.tokens is not None:
            print(' ' * level, "Tokens: ")
            for token in root.tokens:
                print(' ' * level, token.instance)
        if root.children is not None:
            for child in root.children:
                if child is not None:
                    self.PrintTree(child, level + 2)
