from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.Expression.Arithmetic import *

from src.SymbolTable.Types import *
from src.Abstract.Value import *
from src.SymbolTable.Exception import *

class CallArray(Expression):
    
    def __init__(self, id_, poistion_list_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.id = id_
        self.poistion_list = poistion_list_
        self.upper_limit = None
        self.exit_label = None
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        variable = environment_.getVar(self.id)
        
        if variable is None:
            generator.addError(f'La variable < {self.id} > No existe', self.line, self.column)
            return
        if variable.type != Type.ARRAY:
            generator.addError(f'La variable < {self.id} > No es de tipo ARRAY', self.line, self.column)
            return

        generator.addComment(f'--- Inicio < CallArray "{self.id}" >  ---')
        
        # ----------------- VARIABLES TO USE
        temp_move = generator.addTemp()
        temp_result = generator.addTemp()
        value_return = Value(None, None, None)
        self.exit_label = generator.newLabel()
        initial_size = generator.addTemp()
        auxiliar_index = generator.addTemp()
        
        
        temp_pos = variable.pos
        if not variable.isGlobal:
            temp_pos = generator.addTemp()
            generator.addExpression(temp_pos, 'P', variable.pos, "+")
        
        # position at start of array (size)
        generator.getStack(temp_move, temp_pos)
        generator.addExpression(temp_move, temp_move, '1', '+')

        if len(self.poistion_list) == 1:
            index_value = self.poistion_list[0].compile(environment_)
            temp_aux = temp_move
        
            # ----------------- START CONTENT OF CALL
            generator.addExpression(temp_aux, temp_aux, self.getIndex(index_value), '+')
            
            # Save upper limit to BoundsError
            #generator.getStack(initial_size, variable.pos)
            #self.getUpperLimit(initial_size)
            #self.verifyBoundsError(temp_aux, self.upper_limit, temp_result)            
            
            generator.getHeap(temp_result, temp_move)
            
            #generator.putLabel(self.exit_label)
            return Value(temp_result, variable.type_array, True)

        else:
            temp_aux = generator.addTemp()
            
            for i in range(len(self.poistion_list)):
                index_value = self.poistion_list[i].compile(environment_)
                temp_aux = temp_move
                
                # ----------------- START CONTENT OF CALL
                if i == 0:
                    generator.addExpression(temp_aux, temp_aux, self.getIndex(index_value), '+')
                    
                    # Save upper limit to BoundsError
                    #generator.getStack(initial_size, variable.pos)
                    #self.getUpperLimit(initial_size)
                    #self.verifyBoundsError(temp_aux, self.upper_limit, temp_result)
                    continue

                temp_move = generator.addTemp()
                generator.getHeap(temp_move, temp_aux)
                
                generator.addExpression(temp_move, temp_move, '1', '+')
                generator.addExpression(temp_move, temp_move, self.getIndex(index_value), '+')
                
                # Save upper limit to BoundsError
                #self.verifyBoundsError(temp_move, temp_aux, temp_result)
                
            generator.getHeap(temp_result, temp_move)
            generator.addComment("--- Fin < CallArray >  ---")
            
            #generator.putLabel(self.exit_label)
            return Value(temp_result, variable.type_array, True)
    
    def getIndex(self, index_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
        new_value = None
        if index_.is_temp:
            new_value = index_.value
            generator.addExpression(new_value, index_.value, '1', '-')    
        else:
            new_value = index_.value - 1
            
        return new_value
        
    def getUpperLimit(self, temp_move_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        aux = generator.addTemp()
        generator.addExpression(aux, temp_move_, '', '')
        self.upper_limit = aux
        
    def verifyBoundsError(self, index_, upperLimit_, temp_result_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
        label_error = generator.newLabel()
        label_continue = generator.newLabel()
        size = generator.addTemp()
        generator.getHeap(size, upperLimit_)
        
        generator.addIf(index_, '1', '<', label_error)
        generator.addIf(index_, size, '>', label_error)
        generator.addGoto(label_continue)
        
        generator.putLabel(label_error)
        generator.printBoundsError()
        generator.addExpression(temp_result_, '-1', '', '')
        
        generator.addGoto(self.exit_label)
        generator.putLabel(label_continue)