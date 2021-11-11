from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class Truncate(Expression):
    
    def __init__(self, expression_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.expression = expression_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        value: Value = self.expression.compile(environment_)
        #if value.type != Type.FLOAT64:
        #    generator.addError('Se esperaba Float64', self.line, self.column)
        #    return
        
        generator.fTruncFloat()
        generator.addSpace()
        
        tmp_p = generator.addTemp()
        generator.addExpression(tmp_p, 'P', environment_.size, '+')
        generator.addExpression(tmp_p, tmp_p, '1', '+')
        generator.setStack(tmp_p, value.value)
        
        generator.newEnv(environment_.size)
        generator.callFun('truncFloat')
        
        return_p = generator.addTemp()
        generator.getStack(return_p, 'P')
        generator.retEnv(environment_.size)
        
        generator.addSpace()
        
        print(return_p)
        return Value(return_p, Type.INT64, True)