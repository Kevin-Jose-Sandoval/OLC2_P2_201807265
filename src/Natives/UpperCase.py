from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class UpperCase(Expression):
    
    def __init__(self, value_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.value = value_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        self.value.compile(environment_)
        
        generator.fUpperCase()
        param_temp = generator.addTemp()
        generator.addExpression(param_temp, 'P', environment_.size, '+')
    
    
        generator.newEnv(environment_.size)
        generator.callFun('upperCase')
            
        temp = generator.addTemp()
        generator.getStack(temp, 'P')
        generator.retEnv(environment_.size)
            
        return Value(temp, Type.STRING, True)
        