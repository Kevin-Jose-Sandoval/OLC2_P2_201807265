from src.Abstract.Value import Value
from src.Generator.Generator3D import Generator
from src.Abstract.Instruction import *
from src.SymbolTable.Types import *
from src.Instruction.Structs.SymbolStruct import *
from src.Instruction.Structs.ParamStruct import *
from src.SymbolTable.Symbol import *

class AccessStruct(Instruction):
    
    def __init__(self, id_, att_name_list_, line_, column_):
        Instruction.__init__(self, line_, column_)
        self.id = id_
        self.att_name_list = att_name_list_
        
    def compile(self, environment_):
        generator_aux = Generator()
        generator = generator_aux.getInstance()
        
        variable : Symbol = environment_.getVar(self.id)
        
        if variable is None:
            generator.addError(f'No existe la variable <{self.id}>', self.line, self.column)
            return
        
        tmp_i = generator.addTemp()
        tmp_saved = generator.addTemp()
        tmp_pos = variable.pos
        
        i = 0
        att_type = None
        struct: SymbolStruct = environment_.getStruct(variable.type_struct)
        if not variable.isGlobal:
            tmp_pos = generator.addTemp()    
            generator.addExpression(tmp_pos, 'P', variable.pos, '+')
            
        generator.getStack(tmp_i, tmp_pos)
        
        for x in range(len(self.att_name_list)):
            att_search = self.att_name_list[x]
            att_type, i = self.searchAttribute(att_search, struct)
            tmp_aux = tmp_i
            
            if att_type.type == Type.STRUCT:
                struct2: SymbolStruct = environment_.getStruct(att_type.type_aux)
            
                struct = struct2
                
            if x == 0:
                generator.addExpression(tmp_aux, tmp_aux, i, '+')
                continue
            
            tmp_i = generator.addTemp()
            generator.getHeap(tmp_i, tmp_aux)
            generator.addExpression(tmp_i, tmp_i, i, '+')
            
        generator.getHeap(tmp_saved, tmp_i)
        
        value_return = Value(tmp_saved, att_type.type_aux, True)
        if att_type.type_aux == Type.STRUCT:
            value_return.aux_type = att_type.type_aux
        return value_return
            
    
    def searchAttribute(self, att_name_, struct_: SymbolStruct):
        i = 0

        for att in struct_.list_attributes:
            att: ParamStruct
            if att.id == att_name_:
                att_type = att
                return att_type, i
            i += 1
        
        return None, None