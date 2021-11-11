from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class AssignArray(Instruction):
    
    def __init__(self, id_array_, dimensions_, expression_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id_array = id_array_
        self.expression = expression_
        self.dimensions = dimensions_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        variable = environment_.getVar(self.id_array)
        
        if variable is None:
            generator.addError(f'La variable < {self.id_array} > No existe', self.line, self.column)
            return
        if variable.type != Type.ARRAY:
            generator.addError(f'La variable < {self.id_array} > No es de tipo ARRAY', self.line, self.column)
            return

        generator.addComment(f'--- Inicio < AssignArray "{self.id_array}" >  ---')
        
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

        value_expression = self.expression.compile(environment_)

        if len(self.dimensions) == 1:
            index_value = self.dimensions[0].compile(environment_)
            temp_aux = temp_move     
            
            # ----------------- START CONTENT OF CALL
            generator.addExpression(temp_aux, temp_aux, self.getIndex(index_value), '+')
            
            # Save upper limit to BoundsError
            #generator.getStack(initial_size, variable.pos)
            #self.getUpperLimit(initial_size)
            #self.verifyBoundsError(auxiliar_index, self.upper_limit, temp_result)            
            
            #generator.addExpression(temp_move, temp_move, auxiliar_index, '+')
            
            # Assign value
            generator.setHeap(temp_move, value_expression.value)            
            #generator.putLabel(self.exit_label)

        else:
            temp_aux = generator.addTemp()
            
            for i in range(len(self.dimensions)):
                index_value = self.dimensions[i].compile(environment_)
                temp_aux = temp_move
                
                # ----------------- START CONTENT OF CALL
                if i == 0:
                    generator.addExpression(temp_aux, temp_aux, self.getIndex(index_value), '+')
                    
                    #generator.addExpression(auxiliar_index, auxiliar_index, '1', '-')
                    #generator.addExpression(temp_aux, temp_aux, auxiliar_index, '+')
                    
                    # Save upper limit to BoundsError
                    #generator.getStack(initial_size, variable.pos)
                    #self.getUpperLimit(initial_size)
                    #self.verifyBoundsError(auxiliar_index, self.upper_limit, temp_result)
                    continue

                temp_move = generator.addTemp()                
                generator.getHeap(temp_move, temp_aux)
                
                # Save upper limit to BoundsError
                #self.getUpperLimit(temp_move)
                #self.verifyBoundsError(auxiliar_index, self.upper_limit, temp_result)
                generator.addExpression(temp_move, temp_move, '1', '+')
                generator.addExpression(temp_move, temp_move, self.getIndex(index_value), '+')
                
            # Assign value
            generator.setHeap(temp_move, value_expression.value) 
            generator.addComment("--- Fin < AssignArray >  ---")
            
            #generator.putLabel(self.exit_label)
            #return Value(temp_result, variable.type_array, True)

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
        
        generator.addGoto(self.exit_label)
        generator.putLabel(label_continue)