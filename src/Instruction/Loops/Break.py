from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.SymbolTable.Exception import *

class Break(Instruction):
    
    def __init__(self, line_, column_):
        Instruction.__init__(self, line_, column_)
        
    def compile(self, environment_):
        
        if environment_.break_label == '':
            print("BREAK no está en un ciclo")
            return Exception("BREAK no está en un ciclo", self.line, self.column)
        
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        generator.addGoto(environment_.break_label)