from scanner import Scanner, Token, TokenID
import copy

class Stack:
    items = []
    ids = []
    globalDistance = 0

    def push(self, token):
        self.items.append((token, self.globalDistance))
        if token.instance not in self.ids:
            self.ids.append(token.instance)

    def pop(self, distance):
        tempItems = copy.copy(self.items)
        for item in tempItems:
            if item[1] == distance:
                self.items.remove(item)

    def find(self, token):
        for item in self.items:
            if token.instance == item[0].instance:
                return item
        return False


def statSem(root, stack):
    idToken = root.getIdToken()
    if root.name == "vars":
        found = stack.find(idToken)
        if found == False:
            stack.push(idToken)
        elif stack.globalDistance == found[1]:
            raise Exception("Duplicate Declarations",
                            idToken.instance, idToken.line)
    elif idToken is not None:
        found = stack.find(idToken)
        if found == False:
            raise Exception("Variable not Declared",
                            idToken.instance, idToken.line)
    if root.name == "block":
        stack.globalDistance += 1
    if root.children is not None:
        for child in root.children:
            if child is not None:
                statSem(child, stack)
    if root.name == "block":
        stack.pop(stack.globalDistance)
        stack.globalDistance -= 1
    return stack
