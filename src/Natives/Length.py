from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class Length(Expression):
    
    def __init__(self, expression_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.expression = expression_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        value: Value = self.expression.compile(environment_)
        
        if value.type == Type.STRING:
            pass
        else:
            if value.type == Type.ARRAY:
                temp = generator.addTemp()
                length = generator.addTemp()
                
                generator.addSpace()
                generator.addComment('Inicia Length de ARRAY')
                generator.getStack(temp, value.value)
                generator.getHeap(length, temp)
                generator.addSpace()
                generator.addComment('Fin Length de ARRAY')
                
                return Value(length, Type.INT64, True)
            
            else:
                length = generator.addTemp()
                
                generator.addSpace()
                generator.getHeap(length, value.value)
                generator.addSpace()

                return Value(length, Type.INT64, True)