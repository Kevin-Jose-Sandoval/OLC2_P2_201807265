from src.SymbolTable.Generator import *
from src.Abstract.Instruction import *
from src.SymbolTable.Exception import *

class Continue(Instruction):
    
    def __init__(self, line_, column_):
        Instruction.__init__(self, line_, column_)
        
    def compile(self, environment_):

        if environment_.continue_label == '':
            print("CONTINUE no está en un ciclo")
            return Exception("CONTINUE no está en un ciclo", self.line, self.column)

        generator_aux = Generator()
        generator = generator_aux.getInstance()

        generator.addGoto(environment_.continue_label)