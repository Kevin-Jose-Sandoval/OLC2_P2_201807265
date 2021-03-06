from src.Generator.Generator3D import Generator
from src.SymbolTable.Types import Type
from src.SymbolTable.Symbol import *
from src.Instruction.Structs.SymbolStruct import *
from src.SymbolTable.TableObject import *

class Environment:
        
    def __init__(self, previous = None):
        self.previous = previous
        
        self.size = 0
        self.break_label = ''
        self.continue_label = ''
        self.return_label = ''

        if previous is not None:
            self.size = self.previous.size
            self.break_label = self.previous.break_label
            self.continue_label = self.previous.continue_label
        
        self.variables = {}
        self.functions = {}
        self.structs = {}
        self.type = None
        self.scope = None
        
    def saveVar(self, id_var_, type_, in_heap_, type_struct_ = None):
        if id_var_ in self.variables.keys():
            print("Ya existe la variable " + str(id_var_))
            
        else:
            print("----------------", id_var_)
            # (id_, type_, position_, is_global_, in_heap_)
            new_symbol = Symbol(id_var_, type_, self.size, self.previous == None, in_heap_)
            if type_struct_ is not None:
                new_symbol.type_struct = type_struct_
            self.size += 1
            self.variables[id_var_] = new_symbol
        
        # TABLE SYMBOL
        self.addSymbolTable(new_symbol)

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
            print("Funcion repetida < "+ str(id_function_) + " >")
            return True
        else:
            self.functions[id_function_] = function_
            generator_aux = Generator()
            generator = generator_aux.getInstance()            
            generator.symbol_table.append(TableObject(id_function_, self.type, self.scope))            
            return False
            
    def saveStruct(self, id_, list_attributes_, type_struct_ = StructType.INMUTABLE)            :
        if id_ in self.structs.keys():
            return None
        
        new_struct = SymbolStruct(id_, list_attributes_, type_struct_)
        self.structs[id_] = new_struct
        return new_struct
                
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
        
    def getStruct(self, id_):
        env = self
        
        while env != None:
            if id_ in env.structs.keys():
                struct = env.structs[id_]
                return struct

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

    def addSymbolTable(self, symbol):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
                
        if symbol.type == Type.ARRAY:
            generator.symbol_table.append(TableObject(symbol.id, SymbolTableType.ARRAY, self.scope))    
        elif self.type != SymbolTableType.PARAMETER:
            generator.symbol_table.append(TableObject(symbol.id, SymbolTableType.VARIABLE, self.scope))
        else:
            flag = False
            for i in generator.symbol_table:
                if i.name in symbol.id and i.type == SymbolTableType.PARAMETER and i.scope == self.scope:
                    flag = True
            if flag == False:
                generator.symbol_table.append(TableObject(symbol.id, self.type, self.scope))