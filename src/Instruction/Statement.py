from src.Abstract.Instruction import *
from src.Abstract.Value import *
from src.SymbolTable.Environment import *

class Statement(Instruction):
    
    def __init__(self, instructions_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.instructions = instructions_