from src.SymbolTable.Types import *


types_matrix = [
            [Type.INT64,        Type.FLOAT64,       Type.INT64,     Type.CHAR,      Type.ERROR],
            [Type.FLOAT64,      Type.FLOAT64,       Type.ERROR,     Type.ERROR,     Type.ERROR],
            [Type.INT64,        Type.FLOAT64,       Type.BOOLEAN,   Type.ERROR,     Type.ERROR],
            [Type.CHAR,         Type.ERROR,         Type.CHAR,      Type.CHAR,      Type.ERROR],
            [Type.ERROR,        Type.ERROR,         Type.ERROR,     Type.ERROR,     Type.ERROR],
]
            
        
def getTypeMatrix (left_, right_):
    return types_matrix[left_.value][right_.value]