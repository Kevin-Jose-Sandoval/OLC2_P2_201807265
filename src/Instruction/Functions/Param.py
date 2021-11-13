from src.Abstract.Instruction import *

class Param(Instruction):
    
    def __init__(self, id_, type_, line_, column_, type_aux_= None):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.type = type_
        self.type_aux = type_aux_
    
    def compile(self, environment_):
        return self