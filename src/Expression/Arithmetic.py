from src.Generator.Generator3D import Generator
from src.SymbolTable.TypeMatrix import *
from src.Abstract.Expression import *
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
        operation = getArithmeticType(self.type)    # +, -, *, /
        
        if self.type == ArithmeticType.DIV:
            label_true = generator.newLabel()
            label_false = generator.newLabel()
            
            generator.addIf(right_value.value, '0', '!=', label_true)
            generator.printMathError()            
            generator.addExpression(temp, '0', '', '')
            generator.addGoto(label_false)
            generator.putLabel(label_true)
            
            generator.addExpression(temp, left_value.value, right_value.value, operation)
            type_ = getTypeMatrix(left_value.type, right_value.type)
            
            
            result =  Value(temp, type_, True)
            result.false_label = label_false
            
            return result
        
        # POTENCY
        if self.type == ArithmeticType.POWER:
            generator.fPotency()
            param_temp = generator.addTemp()
            generator.addExpression(param_temp, 'P', environment_.size, '+')
            
            # base
            generator.addExpression(param_temp, param_temp, '1', '+')
            generator.setStack(param_temp, left_value.value)
            
            # exponent
            generator.addExpression(param_temp, param_temp, '1', '+')
            generator.setStack(param_temp, right_value.value)            
            
            generator.newEnv(environment_.size)
            generator.callFun('potency')
            
            temp = generator.addTemp()
            generator.getStack(temp, 'P')
            generator.retEnv(environment_.size)

            # return
            return Value(temp, Type.INT, True)

        generator.addExpression(temp, left_value.value, right_value.value, operation)
        type_ = getTypeMatrix(left_value.type, right_value.type)
        
        return Value(temp, type_, True)        