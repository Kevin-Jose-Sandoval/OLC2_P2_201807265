class Exception:
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        
    def toString(self):
        return self.message + " - [" + str(self.line) + "," + str(self.column) + "]"