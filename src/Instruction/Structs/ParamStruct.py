from src.SymbolTable.Types import *

class ParamStruct:
    def __init__(self, id_, type_):
        self.id = id_
        self.type = type_
        self.type_aux = None
        self.verifyType(type_)
        
    def verifyType(self, type):
        self.type_aux = type
        self.type = Type.STRUCT