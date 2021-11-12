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
        generator_aux = Generator()
        generator = generator_aux.getInstance()

        function_ = environment_.getFunction(self.id)

        if function_ is not None:
            param_values = []
            environment_.scope = self.id

            size = generator.saveTemps(environment_)
            
            # compiling parameters values
            for param in self.parametes:
                #environment_.type = SymbolTableType.PARAMETER
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

            #environment_.scope = self.id

            generator.newEnv(environment_.size)
            generator.callFun(self.id)
            generator.getStack(temp, 'P')
            generator.retEnv(environment_.size)
            
            generator.recoverTemps(environment_, size)

            # missing if the function is boolean
            return Value(temp, function_.type, True)

        else:
            generator.addComment(f'Inicio llamada struct < {self.id} >')
            struct = environment_.getStruct(self.id)
            
            if struct is None:
                generator.addError(f'Struct <{self.id}> no existe', self.line, self.column)
                return
            if len(self.parametes) != struct.size_attributes:
                generator.addError('El # de atributos no coincide', self.line, self.column)
                return
            
            self.struct_type = self.id
            
            # save struct pointer
            tmp_saved = generator.addTemp()
            # counter in heap            
            tmp_i_h = generator.addTemp()
            
            generator.addExpression(tmp_saved, 'H', '', '')
            generator.addExpression(tmp_i_h, tmp_saved, '', '')
            
            # save space of struct
            generator.addExpression('H', 'H', struct.size_attributes, '+')
            
            i = 0
            for att in self.parametes:
                att_send = att.compile(environment_)
                att_registered = struct.getAttribute(i)
                
                if att_send.type == Type.BOOLEAN:
                    ret_lb = generator.newLabel()
                    generator.putLabel(att_send.true_label)
                    generator.setHeap(tmp_i_h, '1')
                    generator.addGoto(ret_lb)
                    
                    generator.putLabel(att_send.false_label)
                    generator.setHeap(tmp_i_h, '0')
                    generator.putLabel(ret_lb)
                    
                else:
                    generator.setHeap(tmp_i_h, att_send.value)
                    
                generator.addExpression(tmp_i_h, tmp_i_h, '1', '+')
                i += 1
                
            value_return = Value(tmp_saved, Type.STRUCT, True)
            value_return.aux_type = self.id
            return value_return