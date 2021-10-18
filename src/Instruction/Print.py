from src.Abstract.Instruction import *
from src.SymbolTable.Generator import *
from src.SymbolTable.Types import *

class Print(Instruction):
    
    def __init__(self, value_, line_, column_, new_line_ = False):
        Instruction.__init__(self, line_, column_)
        self.value = value_
        self.new_line = new_line_
    
    def compile(self, environment_):
        value = self.value.compile(environment_)
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        if value.type == Type.INT:
            generator.addPrint("d", value.value)
            
        elif value.type == Type.BOOLEAN:
            exit_label = generator.newLabel()
            
            generator.putLabel(value.true_label)
            generator.printTrue()
            generator.addGoto(exit_label)
            
            generator.putLabel(value.false_label)
            generator.printFalse()
            generator.putLabel(exit_label)

        elif value.type == Type.STRING:
            # call the function to generate the code
            generator.fPrintString()
            # access to simulated environment: t13 = P + size
            paramTemp = generator.addTemp()            
            generator.addExpression(paramTemp, 'P', environment_.size, '+')            
            # increases 1 because index 0 is to return
            generator.addExpression(paramTemp, paramTemp, '1', '+')
            
            # stack[int(paramTemp)] = value.value
            generator.setStack(paramTemp, value.value)
            # change environment: P = P + size
            generator.newEnv(environment_.size)
            generator.callFun('printString')

            # get return value
            temp = generator.addTemp()
            # now P is in printString() environment
            generator.getStack(temp, 'P')
            generator.retEnv(environment_.size)

        else:
            print("Falta en Print")
            
        if self.new_line:
            generator.addPrint("c", 10)