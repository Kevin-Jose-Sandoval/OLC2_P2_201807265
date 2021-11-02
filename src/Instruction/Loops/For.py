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

            # getting ID and initializing the symbol value            
            variable = environment_.getVar(self.id)

            # get position of variable
            temp_pos = variable.pos
            if not variable.isGlobal:
                temp_pos = generator.addTemp()
                # temp_pos = P + position
                generator.addExpression(temp_pos, 'P', variable.pos, "+")            
            generator.setStack(temp_pos, expression1.value)

            # START FOR
            for i in range(int(expression1.value), int(expression2.value) + 1):
                # updating ID                
                generator.setStack(temp_pos, i)                
                result = self.instructions.compile(environment_)
                
            # END FOR
        
        elif self.way_iterate.type_iteration == TypeIteration.STRING:
            # save var
            var = environment_.saveVar(self.id, Type.STRING, False)
                    
            value = self.way_iterate.compile(environment_) # temporary
            temp = self.saveInHeap(value)
            # getting ID          
            variable = environment_.getVar(self.id)
            
            # get position of variable and initialize
            temp_pos = variable.pos
            if not variable.isGlobal:
                temp_pos = generator.addTemp()
                generator.addExpression(temp_pos, 'P', variable.pos, "+")            
            generator.setStack(temp_pos, temp.value)

            temp_move = generator.addTemp()
            generator.addExpression(temp_move, temp_pos, '', '')
            
            for i in range(0, len(value)):
                generator.addExpression(temp_move, temp_move, '1', '+')
                temp = self.saveInHeap(value[i])

                generator.setStack(temp_pos, temp.value)                
                result = self.instructions.compile(environment_)

        generator.addComment("--- Fin < For >  ---")

    def saveInHeap(self, value_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()        
        # ret_temp: value in heap (free value in heap )
        ret_temp = generator.addTemp()
        generator.addExpression(ret_temp, 'H', '', '')

        for char in str(value_):
            generator.setHeap('H', ord(char))
            generator.nextHeap()

        generator.setHeap('H', '-1')
        generator.nextHeap()

        return Value(ret_temp, Type.STRING, True)
            