from src.Abstract.Expression import *
from src.Abstract.Value import *
from src.SymbolTable.Types import *
from src.SymbolTable.Generator import Generator

class Primitive(Expression):
    
    def __init__(self, value_, type_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.value = value_
        self.type = type_

    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
        if self.type == Type.INT or self.type == Type.FLOAT:
            return Value(str(self.value), self.type, False)
        
        elif self.type == Type.BOOLEAN:
            self.checkLabels()
                
            # the result interests 
            if self.value:
                generator.addGoto(self.true_label)
                generator.addComment( "goto "+ str(self.false_label) + ": Para evitar error!")
                generator.addGoto(self.false_label)

            else:
                generator.addGoto(self.false_label)
                generator.addComment( "goto "+ str(self.true_label) + ": Para evitar error!")
                generator.addGoto(self.true_label)

            result = Value(self.value, self.type, False)
            result.true_label = self.true_label
            result.false_label = self.false_label
            
            return result
        
        elif self.type == Type.STRING:
            # ret_temp: value in heap (free value in heap )
            ret_temp = generator.addTemp()
            # ret_temp =  H
            generator.addExpression(ret_temp, 'H', '', '')

            for char in str(self.value):
                # heap[H] = caracter
                generator.setHeap('H', ord(char))
                # H = h + 1
                generator.nextHeap()

            # EOF the string
            generator.setHeap('H', '-1')
            generator.nextHeap()

            # return a temporary
            return Value(ret_temp, Type.STRING, True)
         
        else:
            print("Falta en Primitive")

    def checkLabels(self):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        if self.true_label == '':
            self.true_label = generator.newLabel()
        if self.false_label == '':
            self.false_label = generator.newLabel()            