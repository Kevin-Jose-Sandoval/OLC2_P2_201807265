from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *

class For(Instruction):
    
    def __init__(self, id_, way_iterate_, instructions_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.way_iterate = way_iterate_
        self.instructions = instructions_

    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        generator.addComment("--- Inicio < For >  ---")
        
        if self.way_iterate.type_iteration == TypeIteration.RANK:
            # save var
            var = environment_.saveVar(self.id, Type.INT64, False)
            var.value = 0
            list_rank = self.way_iterate.compile(environment_)
            
            # list_rank -> [[expression1, expression2], WayIterate]
            list_expressions = list_rank[0]      # [expression1, expression2]
            expression1 = list_expressions[0]
            expression2 = list_expressions[1]

            # getting ID          
            variable = environment_.getVar(self.id)

            # get position of variable
            temp_pos = variable.pos
            if not variable.isGlobal:
                temp_pos = generator.addTemp()
                generator.addExpression(temp_pos, 'P', variable.pos, "+")

            # initializing the symbol value
            generator.setStack(temp_pos, expression1.value)

            # ------ CYCLE
            start = generator.newLabel()
            label_true = generator.newLabel()
            exit = generator.newLabel()

            t1 = generator.addTemp()
            t2 = generator.addTemp()
            t3 = generator.addTemp()
            t4 = generator.addTemp()
            t5 = generator.addTemp()

            # ------ cycle start
            generator.putLabel(start)

            generator.addExpression(t2, 'P', temp_pos, '+')
            generator.getStack(t1, t2)
            generator.addIf(t1, expression2.value, '<=', label_true)
            generator.addGoto(exit)

            generator.putLabel(label_true)
            self.instructions.compile(environment_)

            # ------ get and increase variable
            generator.addExpression(t3, 'P', temp_pos, '+')
            generator.getStack(t4, t3)
            generator.addExpression(t5, t4, '1', '+')
            generator.setStack(t3, t5)
            # ------ start again
            generator.addGoto(start)

            generator.putLabel(exit)
            # ------ cycle end 

        elif self.way_iterate.type_iteration == TypeIteration.ARRAY:
            value = self.way_iterate.compile(environment_)

            # save var and getting ID
            variable = environment_.saveVar(self.id, value.type_array, False)

            # get position of variable
            temp_pos = variable.pos
            if not variable.isGlobal:
                temp_pos = generator.addTemp()
                generator.addExpression(temp_pos, 'P', variable.pos, "+")

            # ------ CYCLE
            start = generator.newLabel()
            label_true = generator.newLabel()
            exit = generator.newLabel()

            # pos_array: where start the array in heap
            pos_array = generator.addTemp()
            generator.addExpression(pos_array, value.value, '', '')

            t0 = generator.addTemp()
            size = generator.addTemp()                      
            t1 = generator.addTemp()
            t2 = generator.addTemp()
            counter = generator.addTemp()
            value_array = generator.addTemp()
            index_array = generator.addTemp()

            generator.setStack(temp_pos, value.value)            
            generator.addExpression(counter, '0', '', '')
            # getting size
            generator.getStack(t0, temp_pos)
            generator.getHeap(size, t0)
            

            # initializing the symbol value
            generator.addExpression(counter, '0', '', '')
            generator.addExpression(index_array, pos_array, '', '')
            generator.addExpression(index_array, index_array, '1', '+')
            
            generator.putLabel(start)
            
            generator.addExpression(t2, 'P', temp_pos, '+')
            generator.getStack(t1, t2)
            generator.addIf(counter, size, '<', label_true)
            generator.addGoto(exit)
            
            generator.putLabel(label_true)
            
            # get variable and assign value
            generator.getHeap(value_array, index_array)
            generator.setStack(variable.pos, value_array)
            
            self.instructions.compile(environment_)

            # ------ get and increase variables
            generator.addExpression(counter, counter, '1', '+')
            generator.addExpression(index_array, index_array, '1', '+')
            
            # ------ start again
            generator.addGoto(start)

            generator.putLabel(exit)
            # ------ cycle end             
            
        generator.addComment("--- Fin < For >  ---")