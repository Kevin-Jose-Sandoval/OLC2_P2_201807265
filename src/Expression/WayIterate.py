from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *
from src.Instruction.Arrays.Array import *

class WayIterate(Expression):
    
    def __init__(self, expression1_, expression2_, type_iteration_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.expression1 = expression1_
        self.expression2 = expression2_
        self.type_iteration = type_iteration_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        # expression1 : expression2
        if self.type_iteration == TypeIteration.RANK:
            value1 = self.expression1.compile(environment_)
            value2 = self.expression2.compile(environment_)

            aux_list = []
            aux_list.append(value1)
            aux_list.append(value2)
            
            return aux_list, TypeIteration.RANK
        
        elif self.type_iteration == TypeIteration.STRING:
            
            return self.expression1
        
        elif self.type_iteration == TypeIteration.ARRAY:

            array = Array(self.expression1, self.line, self.column, len(self.expression1))
            value = array.compile(environment_)
            
            # value is a temporary where the array begins
            return value
