from src.SymbolTable.Exception import *
from src.SymbolTable.Types import Type
from src.SymbolTable.Symbol import *
from src.Export import output
from src.SymbolTable.TableObject import *
from src.SymbolTable.Types import *

class Environment:
        
    def __init__(self, previous = None):
        self.previous = previous
        
        self.size = 0
        if previous is not None:
            self.size = self.previous.size
        
        self.variables = {}
        self.functions = {}
        self.structs = {}
        self.type = None
        self.scope = None
        
    def saveVar(self, id_var_, type_, in_heap_):
        if id_var_ in self.variables.keys():
            print("Ya existe la variable " + str(id_var_))
            
        else:
            new_symbol = Symbol(id_var_, type_, self.size, self.previous == None, in_heap_)
            self.size += 1
            self.variables[id_var_] = new_symbol
        
        return self.variables[id_var_] 
        
        
    def saveVarStruct(self, id_var_, attributes_, type_, line_, column_):
        env = self
        new_symbol = Symbol(id_var_,Type.STRUCT, line_, column_, None, type_)
        new_symbol.attributes = attributes_

        while env is not None:
            if id_var_ in env.variables.keys():
                env.variables[id_var_] = new_symbol
                return
            env = env.previous
        self.variables[id_var_] = new_symbol
    
    def saveFunction(self, id_function_, function_):
        if id_function_ in self.functions.keys():
            return True
        else:
            self.functions[id_function_] = function_
            output.symbol_table.append(TableObject(id_function_, self.type, self.scope,
                                                   " Cuerpo función ", function_.line, function_.column))
            return False
            
    def saveStruct(self, id_struct_, attributes_, type_struct_)            :
        if id_struct_ in self.structs.keys():
            return True
        else:
            self.structs[id_struct_] = [attributes_, type_struct_]
            return False
                
    def getVar(self, id_var_):
        env = self
        
        while env is not None:
            if id_var_ in env.variables.keys():
                return env.variables[id_var_]
            
            env = env.previous
        return None
    
    def getFunction(self, id_function_):
        env = self
        
        while env is not None:
            if id_function_ in env.functions.keys():
                return env.functions[id_function_]
            
            env = env.previous
            
        return None
        
    def getStruct(self, id_struct_):
        env = self
        
        while env != None:
            if id_struct_ in env.structs.keys():
                return env.structs[id_struct_]
            
            env = env.previous
            
        return None            
        
    def getGlobal(self):
        env = self
        
        while env.previous is not None:
            env = env.previous
        
        return env
    
    def showVariables(self, env):
        
        for i in env.variables:
            print(i, " , ", str(env.variables[i].value) +" | ", end="")
        print("")                    