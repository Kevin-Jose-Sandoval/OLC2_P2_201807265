from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *

class CallArray(Expression):
    
    def __init__(self, id_, poistion_list_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.id = id_
        self.poistion_list = poistion_list_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        variable = environment_.getVar(self.id)
        a = generator.addTemp()
        
        if variable is None:
            print(f'La variable < {self.id} > No existe')
            return
        
        generator.addComment(f'--- Inicio < CallArray "{self.id}" >  ---')
        
        temp_move = generator.addTemp()
        temp_result = generator.addTemp()
        
        # position at start of array
        generator.getStack(temp_move, variable.pos)        
        generator.addExpression(temp_move, temp_move, '1', '+')
        
        if len(self.poistion_list) == 1:
            index_value = self.poistion_list[0].compile(environment_)
            index = int(index_value.value) - 1
            
            generator.addExpression(temp_move, temp_move, index, '+')
            generator.getHeap(temp_result, temp_move)
            
            return Value(temp_result, Type.INT64, True)
        
        else:
            temp_aux = generator.addTemp()
            
            for i in range(len(self.poistion_list)):
                index_value = self.poistion_list[i].compile(environment_)
                index = int(index_value.value)
                temp_aux = temp_move
                
                if i == 0:
                    generator.addExpression(temp_aux, temp_aux, index - 1, '+')
                    continue

                temp_move = generator.addTemp()                
                generator.getHeap(temp_move, temp_aux)
                generator.addExpression(temp_move, temp_move, index, '+')
                
            generator.getHeap(temp_result, temp_move)
            generator.addComment("--- Fin < CallArray >  ---")
            
            return Value(temp_result, Type.INT64, True)
                
                
                
