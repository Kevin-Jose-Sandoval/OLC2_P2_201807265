from src.Generator.Generator3D import Generator
from src.Abstract.Expression import *
from src.SymbolTable.Types import *
from src.Abstract.Value import *

class Relational(Expression):
    '''
    if expression_true {goto L0;}
    goto L1;
    '''
    def __init__(self, left_, right_, type_, line_, column_):
        Expression.__init__(self, line_, column_)
        self.left = left_
        self.right = right_
        self.type = type_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        generator.addSpace()
        generator.addComment("--- Inicio < Relacional >  ---")
                
        left = self.left.compile(environment_)
        if isinstance(left, Exception): return left
        
        right = None

        result = Value(None, Type.BOOLEAN, False)
        
        if left.type != Type.BOOLEAN:
            right = self.right.compile(environment_)
            
            if (left.type == Type.INT64 or left.type == Type.FLOAT64) and (right.type == Type.INT64 or right.type == Type.FLOAT64):
                self.checkLabels()
                generator.addIf(left.value, right.value, getRelationalType(self.type), self.true_label)
                generator.addGoto(self.false_label)
                
            elif left.type == Type.STRING and right.type == Type.STRING:
                generator.fCompareStr()
                param_temp = generator.addTemp()
                generator.addExpression(param_temp, 'P', environment_.size, '+')
                
                # left_value -> string
                generator.addExpression(param_temp, param_temp, '1', '+')
                generator.setStack(param_temp, left.value)
                
                # right_value  -> string
                generator.addExpression(param_temp, param_temp, '1', '+')
                generator.setStack(param_temp, right.value)            
                
                generator.newEnv(environment_.size)
                generator.callFun('compareStr')
                
                temp = generator.addTemp()
                generator.getStack(temp, 'P')
                generator.retEnv(environment_.size)
                
                # return
                true_label = generator.newLabel()
                false_label = generator.newLabel()
                
                if self.type == RelationalType.EQUAL_EQUAL:                
                    generator.addIf(temp, '0', '==', false_label)
                    generator.addGoto(true_label)
                    
                    result_ = Value(temp, Type.BOOLEAN, True)
                    result_.true_label = true_label
                    result_.false_label = false_label
                    
                    return result_
                if self.type == RelationalType.DISTINCT:
                    generator.addIf(temp, '0', '!=', false_label)
                    generator.addGoto(true_label)
                    
                    result_ = Value(temp, Type.BOOLEAN, True)
                    result_.true_label = true_label
                    result_.false_label = false_label
                    
                    return result_        
        # left.type == BOOLEAN                
        else:
            goto_right = generator.newLabel()
            left_temp = generator.addTemp()
            
            generator.putLabel(left.true_label)
            generator.addExpression(left_temp, '1', '', '')
            generator.addGoto(goto_right)
            
            generator.putLabel(left.false_label)
            generator.addExpression(left_temp, '0', '', '')
            
            generator.putLabel(goto_right)
            
            right = self.right.compile(environment_)
            if right.type != Type.BOOLEAN:
                generator.addError('Relacional: El operando derecho debe ser de tipo BOOLEAN', self.line, self.column)
                return
            
            goto_end = generator.newLabel()
            right_temp = generator.addTemp()
            
            generator.putLabel(right.true_label)
            generator.addExpression(right_temp, '1', '', '')
            generator.addGoto(goto_end)
            
            generator.putLabel(right.false_label)
            generator.addExpression(right_temp, '0', '', '')
            
            generator.putLabel(goto_end)
            
            self.checkLabels()
            generator.addIf(left_temp, right_temp, getRelationalType(self.type), self.true_label)
            generator.addGoto(self.false_label)
            
        generator.addComment("--- Fin < Relacional >  ---")
        generator.addSpace()
                
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