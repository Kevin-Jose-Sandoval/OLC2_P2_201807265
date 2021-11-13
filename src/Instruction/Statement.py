from src.Abstract.Instruction import *

class Statement(Instruction):
    
    def __init__(self, instructions_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.instructions = instructions_
        
    def compile(self, environment_):
        
        for instruction in self.instructions:
            value_return = instruction.compile(environment_)