from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *

class Break(Instruction):
    
    def __init__(self, line_, column_):
        Instruction.__init__(self, line_, column_)
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
        if environment_.break_label == '':
            generator.addError('La sentencia BREAK no está en un ciclo', self.line, self.column)
            return
        
        generator.addGoto(environment_.break_label)