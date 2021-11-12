from src.SymbolTable.Types import *

class TableObject:
    def __init__(self, name_, type_, scope_):
        self.name = name_
        self.type = type_
        self.scope = scope_

    def toString(self):
        if isinstance(self.type, SymbolTableType) and isinstance(self.scope, SymbolTableType):
            return self.name, " - ", self.type.name, " - ", self.scope.name         
        if isinstance(self.type, SymbolTableType):
            return self.name, " - ", self.type.name, " - ", self.scope
        if isinstance(self.scope, SymbolTableType):
            return self.name, " - ", self.type, " - ", self.scope.name     
     
        else:
            return self.name, " - ", self.type, " - ", self.scope