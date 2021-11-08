from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class Length(Expression):
    
    def __init__(self, id_array_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.id_array = id_array_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        # get var
        variable = environment_.getVar(self.id_array)
        
        # get position of variable
        temp_pos = variable.pos
        if not variable.isGlobal:
            temp_pos = generator.addTemp()
            generator.addExpression(temp_pos, 'P', variable.pos, "+")
        
        size = generator.addTemp()
        
        generator.getHeap(size, temp_pos)
        
        return Value(size, Type.INT64, True)