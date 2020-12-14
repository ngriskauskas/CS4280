

class Filter:
    def __init__(self, fileName):
        self.file = open(fileName, 'r')
        self.lines = self.file.readlines()
        self.lineNum = 0
        self.stringNum = 0
        self.numLines = len(self.lines)
        self.file.close()

    def GetNextString(self):
        if self.numLines <= self.lineNum:
            return ("EOF", self.lineNum)
        line = self.lines[self.lineNum].split()
        if len(line) == 0:
            self.lineNum += 1
            self.stringNum = 0
            return self.GetNextString()
        word = line[self.stringNum]
        if word[0] == '#':
            self.lineNum += 1
            self.stringNum = 0
            return self.GetNextString()
        returnVal = (word, self.lineNum)
        if self.stringNum < len(line) - 1:
            self.stringNum += 1
        else:
            self.stringNum = 0
            self.lineNum += 1
        return returnVal
