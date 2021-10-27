from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *

class Access(Expression):
    
    def __init__(self, id_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.id = id_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        generator.addComment("--- Inicio < Compilación acceso > ---")
        var = environment_.getVar(self.id)
        
        if var is None:
            generator.addError(f'No existe la variable < {self.id} >', self.line, self.column)
            return
        
        # temporary to save variable
        temp = generator.addTemp()
        
        # get position of variable
        temp_pos = var.pos
        if not var.isGlobal:
            temp_pos = generator.addTemp()
            # t = P + position
            generator.addExpression(temp_pos, 'P', var.pos, "+")
        # temp = stack[temp_pos]
        generator.getStack(temp, temp_pos)
        
        if var.type != Type.BOOLEAN:
            generator.addComment("--- Fin < Compilación acceso > ---")
            generator.addSpace()
            return Value(temp, var.type, True)
        
        self.checkLabels()

        generator.addIf(temp, '1', '==', self.true_label)
        generator.addGoto(self.false_label)

        generator.addComment("--- Fin < Compilación acceso > ---")
        generator.addSpace()
        
        value_return = Value(None, Type.BOOLEAN, False)
        value_return.true_label = self.true_label
        value_return.false_label = self.false_label

        return value_return
        
    def checkLabels(self):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        if self.true_label == '':
            self.true_label = generator.newLabel()
        if self.false_label == '':
            self.false_label = generator.newLabel()         
            
        
        
        