from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class Declaration(Instruction):
    
    def __init__(self, id_, value_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.value = value_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        generator.addComment("--- Inicio < Compilar valor de variable > ---")
        # id = value
        value = self.value.compile(environment_)
        generator.addComment("--- Fin < Compilar valor de variable > ---")

        # checking if it is in the heap -> saveVar(id_var_, type_, in_heap_)
        new_var = environment_.getVar(self.id)
        if new_var is None:
            in_heap = (value.type == Type.STRING or value.type == Type.STRUCT)
            new_var = environment_.saveVar(self.id, value.type, in_heap)
        new_var.type = value.type
        
        # get position of variable: space where it is 
        temp_pos = new_var.pos
        if not new_var.isGlobal:
            temp_pos = generator.addTemp()
            # temp_pos = P + position
            generator.addExpression(temp_pos, 'P', new_var.pos, "+")
            
        if value.type == Type.BOOLEAN:
            temp_label = generator.newLabel()
            
            # where is True, save 1
            generator.putLabel(value.true_label)
            generator.setStack(temp_pos, "1")
            
            generator.addGoto(temp_label)
            
            # where is False, save 0
            generator.putLabel(value.false_label)
            generator.setStack(temp_pos, "0")

            generator.putLabel(temp_label)
        else:
            generator.setStack(temp_pos, value.value)
        generator.addSpace()            