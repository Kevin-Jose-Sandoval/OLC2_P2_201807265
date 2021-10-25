from src.Generator.Generator3D import Generator
from src.SymbolTable.Exception import *
from src.Abstract.Expression import *
from src.SymbolTable.Types import *

class Return(Expression):
    
    def __init__(self, expression_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.expression = expression_
        
    def compile(self, environment_):
        
        if environment_.return_label == '':
            print("RETURN no está en una función")
            return Exception("RETURN no está en una función", self.line, self.column)            

        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        value = self.expression.compile(environment_)
        
        if value.type == Type.BOOLEAN:
            temp_label = generator.newLabel()
            
            generator.putLabel(value.true_label)
            generator.setStack('P', '1')
            generator.addGoto(temp_label)
            
            generator.putLabel(value.false_label)
            generator.setStack('P', '0')
            generator.putLabel(temp_label)
            
        else:   # is a number
            generator.setStack('P', value.value)
            
        generator.addGoto(environment_.return_label)