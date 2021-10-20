from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.SymbolTable.Types import *
from src.SymbolTable.Exception import *

class If(Instruction):
    
    def __init__(self, condition_, instructions_, line_, column_, else_st_= None):
        Instruction.__init__(self, line_, column_)
        self.condition = condition_
        self.instructions = instructions_
        self.else_st = else_st_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        generator.addComment("--- Inicio < Compilar IF > ---")
        condition = self.condition.compile(environment_)
        
        if condition.type != Type.BOOLEAN:
            print("La condición del IF no es de tipo BOOLEAN")
            return Exception("La condición del IF no es de tipo BOOLEAN", self.line, self.column)
        
        generator.putLabel(condition.true_label)
        self.instructions.compile(environment_)
        
        if self.else_st is not None:
            label_exit_if = generator.newLabel()
            generator.addGoto(label_exit_if)

        generator.putLabel(condition.false_label)
        if self.else_st is not None:
            self.else_st.compile(environment_)
            generator.putLabel(label_exit_if)