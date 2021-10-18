from src.SymbolTable.Generator import *
from src.Abstract.Instruction import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *
from src.SymbolTable.Exception import *
from src.SymbolTable.Environment import *

class While(Instruction):
    
    def __init__(self, condition_, instructions_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.condition = condition_
        self.instructions = instructions_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        continue_label = generator.newLabel()
        generator.putLabel(continue_label)
        
        condition = self.condition.compile(environment_)
        new_environment = Environment(environment_)
        
        # assign labels to the new environment
        new_environment.break_label = condition.false_label
        new_environment.continue_label = continue_label
        
        generator.putLabel(condition.true_label)
        
        # compile instructions
        self.instructions.compile(new_environment)
        generator.addGoto(continue_label)   # start over
        
        generator.putLabel(condition.false_label)