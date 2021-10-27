from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *

class Logical(Expression):
    
    def __init__(self, left_, right_, type_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.left = left_
        self.right = right_
        self.type = type_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        generator.addSpace()                    
        generator.addComment("--- Inicio < Logica >  ---")
                
        self.checkLabels()
        label_union = ''
        
        if self.type == LogicalType.AND:
            label_union = self.left.true_label = generator.newLabel()
            self.right.true_label = self.true_label
            self.left.false_label = self.right.false_label = self.false_label
            
        elif self.type == LogicalType.OR:
            self.left.true_label = self.right.true_label = self.true_label
            label_union = self.left.false_label = generator.newLabel()
            self.right.false_label = self.false_label
        
        elif self.type == LogicalType.NOT:
            # right = None
            self.left.true_label = self.false_label
            self.left.false_label = self.true_label
        
        left = self.left.compile(environment_)
                
        if left.type != Type.BOOLEAN:
            generator.addError('Logica: El operando izquierdo debe ser de tipo BOOLEAN', self.line, self.column)
            return
        
        if self.type != LogicalType.NOT:
            generator.putLabel(label_union)
            right = self.right.compile(environment_)
            
            if isinstance(right, Exception): return right            
            
            if right.type != Type.BOOLEAN:
                generator.addError('Logica: El operando derecho debe ser de tipo BOOLEAN', self.line, self.column)
                return
        
        generator.addComment("--- Fin < Logica >  ---")        
        generator.addSpace()
        
        result = Value(None, Type.BOOLEAN, False)
        result.true_label = self.true_label
        result.false_label = self.false_label
        
        return result
    
    def checkLabels(self):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        if self.true_label == '':
            self.true_label = generator.newLabel()
        if self.false_label == '':
            self.false_label = generator.newLabel()