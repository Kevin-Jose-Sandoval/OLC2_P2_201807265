from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *

class Param(Instruction):
    
    def __init__(self, id_, type_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.type = type_
    
    def compile(self, environment_):
        return self