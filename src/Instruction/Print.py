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
            generator.fPrintString()

            paramTemp = generator.addTemp()
            
            generator.addExpression(paramTemp, 'P', environment_.size, '+')
            # value 0 is to return, because increases 1
            generator.addExpression(paramTemp, paramTemp, '1', '+')
            generator.setStack(paramTemp, value.value)
            
            generator.newEnv(environment_.size)
            generator.callFun('printString')

            # get return
            temp = generator.addTemp()
            generator.getStack(temp, 'P')
            generator.retEnv(environment_.size)

        else:
            print("Falta en Print")
            
        if self.new_line:
            generator.addPrint("c", 10)