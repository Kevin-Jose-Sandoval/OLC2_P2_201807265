from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *

class CallFunction(Expression):
    
    def __init__(self, id_, parameters_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.id = id_
        self.parametes = parameters_
        
    def compile(self, environment_):
        function_ = environment_.getFunction(self.id)
        
        if function_ is not None:
            param_values = []
            
            generator_aux = Generator()
            generator = generator_aux.getInstance()
            
            size = generator.saveTemps(environment_)
            
            # compiling parameters values
            for param in self.parametes:
                param_values.append(param.compile(environment_))
            
            temp = generator.addTemp()            
            generator.addExpression(temp, 'P', environment_.size + 1, '+')
            aux = 0

            # setStack of parameters values
            for param in param_values:
                aux = aux + 1
                generator.setStack(temp, param.value)

                if aux != len(param_values):
                    generator.addExpression(temp, temp, '1', '+')

            generator.newEnv(environment_.size)
            generator.callFun(self.id)
            generator.getStack(temp, 'P')
            generator.retEnv(environment_.size)
            
            generator.recoverTemps(environment_, size)

            # missing if the function is boolean
            return Value(temp, function_.type, True)

        else:
            print("Llamada a un STRUCT")