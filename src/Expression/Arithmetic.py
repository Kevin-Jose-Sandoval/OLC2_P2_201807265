from src.Abstract.Expression import *
from src.SymbolTable.Generator import *
from src.SymbolTable.Exception import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *

class Arithmetic(Expression):
    
    def __init__(self, left_, right_, type_, line_, column_):
        Expression.__init__(self, line_, column_)    
        self.left = left_
        self.right = right_
        self.type = type_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        left_value = self.left.compile(environment_)
        right_value = self.right.compile(environment_)
        
        if isinstance(left_value, Exception): return left_value
        if isinstance(right_value, Exception): return right_value

        temp = generator.addTemp()
        operation = getArithmeticType(self.type)

        generator.addExpression(temp, left_value.value, right_value.value, operation)
        return Value(temp, Type.INT, True)