from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.Expression.Primitive import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class Array(Instruction):
    
    def __init__(self, list_expr_, line_, column_, size_ = None):
        Instruction.__init__(self, line_, column_)
        self.expressions_list = list_expr_
        self.size = size_
        self.values_list = []
        self.type = None
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        generator.addComment("--- Inicio < Guardar Array >  ---")
        
        temp = generator.addTemp()
        temp_move = generator.addTemp()
        
        generator.addExpression(temp, 'H', '', '')
        generator.addExpression(temp_move, temp, '1', '+')
        
        generator.setHeap('H', len(self.expressions_list) )     # save array size
        generator.addExpression('H', 'H', self.size + 1, '+')

        for expression in self.expressions_list:            
            value = expression.compile(environment_)
            
            if isinstance(expression, Primitive):
                self.type = value.type
            
            generator.setHeap(temp_move, value.value)            
            generator.addExpression(temp_move, temp_move, '1', '+')
            
            if value.type == Type.ARRAY:
                self.values_list.append(value.getValuesArray())
            else:     
                self.values_list.append(value.value)

        generator.list_aux.append(self.values_list)
        
        generator.addComment("--- Fin < Guardar Array >  ---")
        result = Value(temp, Type.ARRAY, True)
        result.type_array = self.type
        
        return result