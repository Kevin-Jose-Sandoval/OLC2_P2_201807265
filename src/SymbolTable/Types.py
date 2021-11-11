from enum import Enum

class TypeIteration(Enum):
    RANK = 0
    STRING = 1
    ID = 2
    ARRAY = 3
    STRUCT = 4
    
class TypeNative(Enum):
    # mathematics
    LOG_10 = 0
    LOG_N = 1
    SIN = 2
    COS = 3
    TAN = 4    
    SQUARE_ROOT = 5
    # data management
    UPPER = 6
    LOWER = 7
    PARSE = 8
    TRUNC = 9
    FLOAT = 10
    STRING = 11
    TYPE_OF = 12
    # arrays
    PUSH = 13
    POP = 14
    LENGTH = 15
    
class Type(Enum):
    INT64 = 0
    FLOAT64 = 1
    BOOLEAN = 2
    CHAR = 3
    STRING = 4
    
    NULL = 5  
    ARRAY = 6
    STRUCT = 7
    UNDEFINED = 8
    
    RETURN_ST = 9
    CONTINUE_ST = 10
    BREAK_ST = 11
    
    ERROR = 12

class ArithmeticType(Enum):
    PLUS = 0    # +
    MINUS = 1   # -
    TIMES = 2   # *
    DIV = 3     # /
    UMINUS = 4  # -
    POWER = 5   # **
    MOD = 6     # %
    COMMA = 7   # ,
    
class RelationalType(Enum):
    GREATER = 0           # >
    LESS = 1              # <
    GREATER_EQUAL = 2     # >=
    LESS_EQUAL = 3        # <=
    EQUAL_EQUAL = 4       # ==
    DISTINCT = 5          # !=

class LogicalType(Enum):
    AND = 0     # &&
    OR = 1      # ||
    NOT = 2     # !

class SymbolTableType(Enum):
    GLOBAL = 0
    VARIABLE = 1
    ARRAY = 2
    FUNCTION = 3
    PARAMETER = 4

class ScopeType(Enum):
    GLOBAL = 0
    LOCAL = 1
    
class StructType(Enum):
    MUTABLE = 0
    INMUTABLE = 1

# ========================== FUNCTIONS ==========================
def getType(type_):
    if type_ == Type.INT:
        return 'Int64'
    elif type_ == Type.FLOAT:
        return 'Float64'
    elif type_ == Type.BOOLEAN:
        return 'Bool'
    elif type_ == Type.CHAR:
        return 'Char'    
    elif type_ == Type.STRING:
        return 'String'
    elif type_ == Type.NULL:
        return 'nothing'
    
def getArithmeticType(type_):
    if type_ == ArithmeticType.PLUS:
        return '+'
    elif type_ == ArithmeticType.MINUS:
        return '-'
    elif type_ == ArithmeticType.TIMES:
        return '*'
    elif type_ == ArithmeticType.DIV:
        return '/'
    elif type_ == ArithmeticType.MOD:
        return '%'  
    
def getRelationalType(type_):
    if type_ == RelationalType.GREATER:
        return '>'
    elif type_ == RelationalType.LESS:
        return '<'
    elif type_ == RelationalType.GREATER_EQUAL:
        return '>='
    elif type_ == RelationalType.LESS_EQUAL:
        return '<='
    elif type_ == RelationalType.EQUAL_EQUAL:
        return '=='
    elif type_ == RelationalType.DISTINCT:
        return '!='
    
def getLogicalType(type_):
    if type_ == LogicalType.AND:
        return '&&'
    if type_ == LogicalType.OR:
        return '||'
    if type_ == LogicalType.NOT:
        return '!'
    
    return None