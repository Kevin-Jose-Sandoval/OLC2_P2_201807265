from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.SymbolTable.Types import *

class Struct(Instruction):
    
    def __init__(self, id_, list_attributes_, line_, column_, type_ = StructType.INMUTABLE):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.list_attributes = list_attributes_
        self.type = type_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
        struct_simbol = environment_.saveStruct(self.id, self.list_attributes, self.type)
        
        if struct_simbol is None:
            generator.addError(f'El struct < {self.id} > ya existe', self.line, self.column)
            return