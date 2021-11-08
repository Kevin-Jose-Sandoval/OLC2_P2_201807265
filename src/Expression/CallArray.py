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
        
        # position at start of array (size)
        generator.getStack(temp_move, variable.pos)
        generator.addExpression(temp_move, temp_move, '1', '+')

        if len(self.poistion_list) == 1:
            index_value = self.poistion_list[0].compile(environment_)
            
            # ----------------- VERIFICATON OF INDEX (TEMP  || INT)
            if index_value.is_temp:
                # auxiliar_index has a temporaly with index value
                generator.addExpression(auxiliar_index, index_value.value, '', '')
                temp_aux = temp_move
                
            else:
                index = int(index_value.value)
                generator.addExpression(auxiliar_index, index, '', '')
                temp_aux = temp_move            
            
            # ----------------- START CONTENT OF CALL
            generator.addExpression(auxiliar_index, auxiliar_index, '1', '-')
            
            # Save upper limit to BoundsError
            generator.getStack(initial_size, variable.pos)
            self.getUpperLimit(initial_size)
            self.verifyBoundsError(auxiliar_index, self.upper_limit, temp_result)            
            
            generator.addExpression(temp_move, temp_move, auxiliar_index, '+')
            generator.getHeap(temp_result, temp_move)
            
            generator.putLabel(self.exit_label)
            return Value(temp_result, variable.type_array, True)

        else:
            temp_aux = generator.addTemp()
            
            for i in range(len(self.poistion_list)):
                index_value = self.poistion_list[i].compile(environment_)
                
                # ----------------- VERIFICATON OF INDEX (TEMP  || INT)
                if index_value.is_temp:
                    # auxiliar_index has a temporaly with index value
                    generator.addExpression(auxiliar_index, index_value.value, '', '')
                    temp_aux = temp_move
                    
                else:
                    index = int(index_value.value)
                    generator.addExpression(auxiliar_index, index, '', '')
                    temp_aux = temp_move
                
                # ----------------- START CONTENT OF CALL
                if i == 0:
                    generator.addExpression(auxiliar_index, auxiliar_index, '1', '-')
                    generator.addExpression(temp_aux, temp_aux, auxiliar_index, '+')
                    
                    # Save upper limit to BoundsError
                    generator.getStack(initial_size, variable.pos)
                    self.getUpperLimit(initial_size)
                    self.verifyBoundsError(auxiliar_index, self.upper_limit, temp_result)
                    continue

                temp_move = generator.addTemp()                
                generator.getHeap(temp_move, temp_aux)
                
                # Save upper limit to BoundsError
                self.getUpperLimit(temp_move)
                self.verifyBoundsError(auxiliar_index, self.upper_limit, temp_result)

                generator.addExpression(temp_move, temp_move, auxiliar_index, '+')
                
            generator.getHeap(temp_result, temp_move)
            generator.addComment("--- Fin < CallArray >  ---")
            
            generator.putLabel(self.exit_label)
            return Value(temp_result, variable.type_array, True)
        
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
        
        generator.addIf(index_, '0', '<', label_error)
        generator.addIf(index_, size, '>', label_error)
        generator.addGoto(label_continue)
        
        generator.putLabel(label_error)
        generator.printBoundsError()
        generator.addExpression(temp_result_, '-1', '', '')
        
        generator.addGoto(self.exit_label)
        generator.putLabel(label_continue)