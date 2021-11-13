from src.Generator.Generator3D import Generator
from src.SymbolTable.Exception import *
from src.SymbolTable.Environment import *
from src.Abstract.Instruction import *
from src.SymbolTable.Types import *
from src.SymbolTable.Symbol import *

class Function(Instruction):
    
    def __init__(self, id_, parameters_, type_, instructions_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.parameters = parameters_
        self.type = type_
        self.instructions = instructions_
        
    def compile(self, environment_):
        environment_.scope = SymbolTableType.GLOBAL
        environment_.type = SymbolTableType.FUNCTION  
                
        environment_.saveFunction(self.id, self)        
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        new_env = Environment(environment_)
                    
        return_label = generator.newLabel()
        new_env.return_label = return_label
        new_env.size = 1

        for param in self.parameters:
            new_env.type = SymbolTableType.PARAMETER
            new_env.scope = self.id
            
            in_heap_ = (param.type == Type.STRING or param.type == Type.STRUCT)
            
            if isinstance(param.type, Type) and param.type_aux != Type.ARRAY:
                new_env.saveVar(param.id, param.type, in_heap_)
            elif isinstance(param.type, Type) and param.type_aux == Type.ARRAY:
                var :Symbol  = new_env.saveVar(param.id, Type.ARRAY, in_heap_)
                var.type_array = param.type
            else:
                new_env.saveVar(param.id, Type.STRUCT, in_heap_, param.type)

        generator.freeAllTemps()
        generator.addBeginFunc(self.id)

        new_env.type = None       
        self.instructions.compile(new_env)
        
        if self.type is not None:
            generator.putLabel(return_label)

        generator.addEndFunc()
        generator.freeAllTemps()
        