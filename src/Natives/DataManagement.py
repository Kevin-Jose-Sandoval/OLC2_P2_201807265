from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class DataManagement(Expression):
    
    def __init__(self, type_function_, expression_, line_, column_, type_ = None):
        Expression.__init__(self, line_, column_)
        self.type_function = type_function_
        self.expression = expression_
        self.type_parse = type_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        # trunc: float -> int not rounded
        if self.type_function == TypeNative.TRUNC:
            value = self.expression.compile(environment_)
            
            # value.value in this moment is string
            value_float = float(value.value)
            value_int = int(value_float)
            
            return Value(value_int, Type.INT64, False)
        
        # float(num_int): int -> float
        elif self.type_function == TypeNative.FLOAT:
            value = self.expression.compile(environment_)
            # value.value in this moment is string
            value_float = float(value.value)
            
            return Value(value_float, Type.FLOAT64, False)
        
        # string(any_type): any_type -> string
        elif self.type_function == TypeNative.STRING:
            value = self.expression.compile(environment_)
            
            # ret_temp: value in heap (free value in heap )
            ret_temp = generator.addTemp()
            # ret_temp =  H
            generator.addExpression(ret_temp, 'H', '', '')

            for char in str(value.value):
                # heap[H] = caracter
                generator.setHeap('H', ord(char))
                # H = h + 1
                generator.nextHeap()

            # EOF the string
            generator.setHeap('H', '-1')
            generator.nextHeap()

            # return a temporary
            return Value(ret_temp, Type.STRING, True)

        # parse string -> numeric
        elif self.type_function == TypeNative.PARSE:
            
            if self.type_parse == Type.INT64:
                value_float = float(self.expression.value)            
                value_int = int(value_float)
                
                return Value(value_int, Type.INT64, False)
            
            elif self.type_parse == Type.FLOAT64:
                value_float = float(self.expression.value)            
                
                return Value(value_float, Type.FLOAT64, False)            
            