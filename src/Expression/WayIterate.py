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

        if self.type_iteration == TypeIteration.STRUCT:
            value = self.expression1.compile(environment_)
            #print(value.value, value.type, '=====', value.type_array, '**')
            
            # value.value start the array
            # considering that it will always be an array
            value.type_array = value.type
            
            value_return = Value(value.value, Type.ARRAY, True)
            value_return.type_array = value.type_array
            
            return value_return
            
        # expression1 : expression2
        elif self.type_iteration == TypeIteration.RANK:
            value1 = self.expression1.compile(environment_)
            value2 = self.expression2.compile(environment_)

            aux_list = []
            aux_list.append(value1)
            aux_list.append(value2)
            
            return aux_list, TypeIteration.RANK
        
        elif self.type_iteration == TypeIteration.STRING:
            
            primitive = Primitive(str(self.expression1), Type.STRING, self.line, self.column)
            value = primitive.compile(environment_)

            # value is a temporary where the string begins            
            return value
        
        elif self.type_iteration == TypeIteration.ARRAY:

            array = Array(self.expression1, self.line, self.column, len(self.expression1))
            value = array.compile(environment_)
            
            # value is a temporary where the array begins
            return value

        elif self.type_iteration == TypeIteration.ID:
            # can be a STRING or ARRAY
            
            # found a position where is start
            position = generator.addTemp()
            variable = environment_.getVar(str(self.expression1))
            generator.getStack(position, variable.pos)
            
            if variable.type == Type.ARRAY:
                result = Value(position, variable.type, True)
                result.type_array = variable.type_array
                
                return result
            
            if variable.type == Type.STRING:
                
                return Value(position, variable.type, True)
            
        elif self.type_iteration is None:
            value = self.expression1.compile(environment_)
            #print('***',value.aux_type, value.value, value.type, value.type_array)
            
            return value
            