from src.SymbolTable.Types import *

class SymbolStruct:
    def __init__(self, id_, list_attributes_, type_struct_ = StructType.INMUTABLE):
        self.id = id_
        self.list_attributes = list_attributes_
        self.size_attributes = len(list_attributes_)
        self.type_struct = type_struct_
        
    def getAttribute(self, index_):
        att = self.list_attributes[index_]
        return att