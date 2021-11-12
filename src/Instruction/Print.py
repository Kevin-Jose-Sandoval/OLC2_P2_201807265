from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.SymbolTable.Types import *

class Print(Instruction):
    
    def __init__(self, value_, line_, column_, new_line_ = False):
        Instruction.__init__(self, line_, column_)
        self.value = value_
        self.new_line = new_line_
    
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        if self.value is None:
            generator.addPrint("c", 10)
            #generator.addError(f'Print no puede imprimir None', self.line, self.column)
            #return            
        else:
        
            if len(self.value) == 1:
                value = self.value[0].compile(environment_)

               # generator.printValueHeap(value.value)
                if value.type == Type.INT64:
                    generator.addPrint("d", value.value)

                elif value.type == Type.FLOAT64:
                    generator.addPrintFloat("g", value.value)
                    
                elif value.type == Type.BOOLEAN:
                    self.typeBoolean(value)

                elif value.type == Type.STRING:
                    self.typeString(value, environment_)

                elif value.type == Type.CHAR:
                    generator.addPrint("c", value.value)
                
                else:
                    print("Falta en Print")
                    
                if self.new_line:
                    generator.addPrint("c", 10)
            
            else:
                for i in self.value:
                    value = i.compile(environment_)
                    
                    if value.type == Type.INT64:
                            generator.addPrint("d", value.value)

                    elif value.type == Type.FLOAT64:
                        generator.addPrintFloat("f", value.value)
                        
                    elif value.type == Type.BOOLEAN:
                        self.typeBoolean(value)

                    elif value.type == Type.STRING:
                        self.typeString(value, environment_)

                    elif value.type == Type.CHAR:
                        generator.addPrint("c", value.value)
                    
                    else:
                        print("Falta en Print")
                        
                if self.new_line:
                    generator.addPrint("c", 10)
                
            
    def typeBoolean(self, value):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        exit_label = generator.newLabel()
        
        generator.putLabel(value.true_label)
        generator.printTrue()
        generator.addGoto(exit_label)
        
        generator.putLabel(value.false_label)
        generator.printFalse()
        generator.putLabel(exit_label)
        
    def typeString(self, value, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
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