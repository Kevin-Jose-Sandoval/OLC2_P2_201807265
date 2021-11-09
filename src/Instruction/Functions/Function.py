from src.Generator.Generator3D import Generator
from src.SymbolTable.Exception import *
from src.SymbolTable.Environment import *
from src.Abstract.Instruction import *
from src.SymbolTable.Types import *

class Function(Instruction):
    
    def __init__(self, id_, parameters_, type_, instructions_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.parameters = parameters_
        self.type = type_
        self.instructions = instructions_
        
    def compile(self, environment_):
        
        environment_.saveFunction(self.id, self)        
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        new_env = Environment(environment_)
        
        return_label = generator.newLabel()
        new_env.return_label = return_label
        new_env.size = 1
        
        for param in self.parameters:
            in_heap_ = (param.type == Type.STRING or param.type == Type.STRUCT)
            new_env.saveVar(param.id, param.type, in_heap_)
            
        generator.freeAllTemps()
        generator.addBeginFunc(self.id)
        
        try:
            self.instructions.compile(new_env)
        except:
            print("Error al compilar instrucciones de < "+ self.id + " >")
        
        if self.type is not None:
            generator.putLabel(return_label)

        generator.addEndFunc()
        generator.freeAllTemps()