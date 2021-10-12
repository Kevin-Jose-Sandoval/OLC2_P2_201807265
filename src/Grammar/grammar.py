# imports
# general
from src.SymbolTable.Types import *
from src.SymbolTable.Exception import *

# instructions
from src.Instruction.Statement import *
from src.Instruction.Print import *
"""
from src.Instruction.Conditional.If import *
from src.Instruction.Loops.While import *
from src.Instruction.Variables.Declaration import *
from src.Instruction.Functions.Return import *
from src.Instruction.Loops.Break import *
from src.Instruction.Loops.Continue import *
from src.Instruction.Functions.Function import *
from src.Instruction.Functions.Param import *
from src.Instruction.Arrays.Array import *
from src.Instruction.Arrays.AssignArray import *
from src.Instruction.Loops.For import *
from src.Instruction.Structs.DeclareStruct import *
from src.Instruction.Structs.CreateStruct import *
from src.Instruction.Structs.AssignAccess import * 
"""

# expressions
from src.Expression.Arithmetic import *
from src.Expression.Primitive import *
from src.Expression.Relational import *
from src.Expression.Logical import *
""" 
from src.Expression.Access import *
from src.Expression.CallFunction import *
from src.Natives.Mathematic import *
from src.Natives.DataManagement import *
from src.Expression.CallArray import *
from src.Natives.NativeArray import *
from src.Expression.WayIterate import *
from src.Expression.AccessStruct import *
"""

errors = []

# ========================== LEXICAL ANALYSIS ==========================
reserved_words = {
    # general reserved words
    'end'       : 'END',
    'true'      : 'TRUE',
    'false'     : 'FALSE',
    'global'    : 'GLOBAL',
    
    # types
    'Int64'     : 'TYPE_INT64',
    'Float64'   : 'TYPE_FLOAT64',
    'Bool'      : 'TYPE_BOOL',
    'Char'      : 'TYPE_CHAR',
    'String'    : 'TYPE_STRING',
    'Nothing'   : 'TYPE_NOTHING',
    
    # if sentence
    'if'        : 'IF',
    'elseif'    : 'ELSE_IF',
    'else'      : 'ELSE',
    
    # while sentence
    'while'     : 'WHILE',
    'break'     : 'BREAK',
    'continue'  : 'CONTINUE',
    
    # functions sentence
    'function'  : 'FUNCTION',
    'return'    : 'RETURN',
    
    # natives
    'println'   : 'PRINTLN',
    'print'     : 'PRINT',
    
    # native mathematics
    'sqrt'      : 'SQUARE_ROOT',
    'log10'     : 'LOG_10',
    'log'       : 'LOG_N',
    'sin'       : 'SIN',
    'cos'       : 'COS',
    'tan'       : 'TAN',
    'uppercase' : 'UPPER',
    'lowercase' : 'LOWER',
    
    # native data management
    'parse'     : 'PARSE',
    'trunc'     : 'TRUNC',
    'float'     : 'FLOAT',
    'string'    : 'STRING',
    'typeof'    : 'TYPE_OF',
    
    # natives arrays
    'push'      : 'PUSH',
    'pop'       : 'POP',
    'length'    : 'LENGTH',
    
    # for sentence
    'in'        : 'IN',
    'for'       : 'FOR',
    
    # struct sentence
    'struct'    : 'STRUCT',
    'mutable'   : 'MUTABLE'
}

tokens = [
    'ID',
    
    # native values
    'PRIMITIVE_INT',
    'PRIMITIVE_FLOAT',
    'PRIMITIVE_STRING',
    'PRIMITIVE_CHAR',
    
    # general symbols
    'EQUAL',
    'COLON',
    'POINT',
    'SEMICOLON',
    'COMMA',
    'LEFT_PAR',
    'RIGHT_PAR',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    
    # arithmetics symbols
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',
    'POWER',
    'MOD',
    
    # logical symbols
    'AND',
    'OR',
    'NOT',
    
    # relational symbols
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    'EQUAL_EQUAL',
    'DISTINCT'

] + list(reserved_words.values())

# TOKENS 
# general symbols
t_EQUAL                 = r'='
t_COLON                 = r':'
t_POINT                 = r'\.'
t_SEMICOLON             = r';'
t_COMMA                 = r','
t_LEFT_PAR              = r'\('
t_RIGHT_PAR             = r'\)'
t_LEFT_BRACKET          = r'\['
t_RIGHT_BRACKET         = r'\]'

# arithmetics symbols
t_PLUS                  = r'\+'
t_MINUS                 = r'-'
t_TIMES                 = r'\*'
t_DIV                   = r'/'
t_POWER                 = r'\^'
t_MOD                   = r'\%'
# logical symbols
t_AND                   = r'&&'
t_OR                    = r'\|\|'
t_NOT                   = r'!'

# relational symbols
t_GREATER               = r'>'
t_LESS                  = r'<'
t_GREATER_EQUAL         = r'>='
t_LESS_EQUAL            = r'<='
t_EQUAL_EQUAL           = r'=='
t_DISTINCT              = r'!='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value, 'ID')
    return t

def t_PRIMITIVE_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error in parse to float")
        t.value = 0
    return t

def t_PRIMITIVE_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error in parse to int")
        t.value = 0
    return t

def t_PRIMITIVE_CHAR(t):
    r'(\'([a-zA-Z]|\\\'|\\"|\\t|\\n|\\\\|.)\')'
    t.value = t.value[1:-1]
    return t

def t_PRIMITIVE_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_MULTILINE_COMMENT(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count("\n")

def t_ONE_LINE_COMMENT(t):
    r'\#.*\n'
    t.lexer.lineno += 1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):    
    if t.value[0] != ' ':
        print("Illegal character '%s'" % t.value[0])
        #errors.append(Exception("Léxico", "Caracter " + t.value[0] + " no pertenece al lenguaje", t.lexer.lineno, find_column(input_, t)))
    t.lexer.skip(1)
   
def find_column(input_, token_):
    line_start = input_.rfind('\n', 0, token_.lexpos) + 1
    return (token_.lexpos - line_start) + 1

import ply.lex as lex
lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right','UNOT'),
    ('left', 'EQUAL_EQUAL', 'DISTINCT'),
    ('left', 'GREATER', 'GREATER_EQUAL','LESS','LESS_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'MOD'),
    ('left', 'POWER'),    
    ('right', 'UMINUS'),
)

# ========================== SYNTACTIC ANALYSIS ==========================
def p_start(t):
    'start : instructions'
    t[0] = t[1]
    return t[0]

def p_instructions(t):
    '''
    instructions : instructions instruction
                 | instruction
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_instruction(t):
    '''
    instruction : print_st SEMICOLON
    '''
    t[0] = t[1]

# ------------------------------ STATEMENT
def p_statement(t):
    '''statement : instructions'''
    t[0] = Statement(t[1], t.lineno(1), t.lexpos(0))

# ------------------------------ ERROR
def p_instruccion_error(t):
    'instruction : error SEMICOLON'
    
    print("Error sintáctico: ", str(t[1].value))
    errors.append(
        Exception("Sintáctico", "En la instruccion: " + str(t[1].value), t.lineno(1), find_column(input_, t.slice[1])))
    t[0] = ""
    
# ------------------------------ PRINT
def p_println_st(t):
    'print_st : PRINTLN LEFT_PAR expression RIGHT_PAR'
    t[0] = Print(t[3], t.lineno(1), find_column(input_, t.slice[1]), True)
                
# ------------------------------ EXPRESSIONS
def p_expression(t):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIV expression
               | expression POWER expression
               | expression MOD expression               

               | expression GREATER expression
               | expression LESS expression
               | expression GREATER_EQUAL expression
               | expression LESS_EQUAL expression
               | expression EQUAL_EQUAL expression
               | expression DISTINCT expression
               
               | expression AND expression
               | expression OR expression
                                  
    '''
    if t[2] == '+':
        t[0] = Arithmetic( t[1], t[3], ArithmeticType.PLUS, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '-':
        t[0] = Arithmetic( t[1], t[3], ArithmeticType.MINUS, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '*':
        t[0] = Arithmetic( t[1], t[3], ArithmeticType.TIMES, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '/':
        t[0] = Arithmetic( t[1], t[3], ArithmeticType.DIV, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '^':
        t[0] = Arithmetic( t[1], t[3], ArithmeticType.POWER,  t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '%':
        t[0] = Arithmetic( t[1], t[3], ArithmeticType.MOD, t.lineno(2), find_column(input_, t.slice[2]))

    elif t[2] == '==':
        t[0] = Relational(t[1], t[3], RelationalType.EQUAL_EQUAL, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relational(t[1], t[3], RelationalType.DISTINCT, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relational(t[1], t[3], RelationalType.LESS, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relational(t[1], t[3], RelationalType.GREATER, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relational(t[1], t[3], RelationalType.LESS_EQUAL, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relational(t[1], t[3], RelationalType.GREATER_EQUAL, t.lineno(2), find_column(input_, t.slice[2]))        

    elif t[2] == '&&':
        t[0] = Logical(t[1], t[3], LogicalType.AND, t.lineno(2), find_column(input_, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logical(t[1], t[3], LogicalType.OR, t.lineno(2), find_column(input_, t.slice[2]))       
        
def p_expression_parenthesis(t):
    'expression : LEFT_PAR expression RIGHT_PAR'
    t[0] = t[2]

def p_unary_operation(t):
    '''
    expression : MINUS expression %prec UMINUS
               | NOT expression %prec UNOT
    '''
    if t[1] == '-':
        t[0] = Arithmetic(Primitive(0, Type.INT, t.lineno(1), find_column(input_, t.slice[1])),
                          t[2], ArithmeticType.MINUS, t.lineno(1), find_column(input_, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logical(t[2], None, LogicalType.NOT, t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ EXPRESSIONS - PRIMITIVES
def p_primitive_int(t):
    'expression : PRIMITIVE_INT'
    t[0] = Primitive(int(t[1]), Type.INT, t.lineno(1), find_column(input_, t.slice[1]))

def p_primitive_float(t):
    'expression : PRIMITIVE_FLOAT'
    t[0] = Primitive(float(t[1]), Type.FLOAT, t.lineno(1), find_column(input_, t.slice[1]))

def p_primitive_string(t):
    'expression : PRIMITIVE_STRING'
    t[0] = Primitive(str(t[1]), Type.STRING, t.lineno(1), find_column(input_, t.slice[1]))
    
def p_primitive_char(t):
    'expression : PRIMITIVE_CHAR'
    t[0] = Primitive(str(t[1]), Type.CHAR, t.lineno(1), find_column(input_, t.slice[1]))
            
def p_primitive_true(t):
    'expression : TRUE'
    t[0] = Primitive(True, Type.BOOLEAN, t.lineno(1), find_column(input_, t.slice[1]))
    
def p_primitive_false(t):
    'expression : FALSE'
    t[0] = Primitive(False, Type.BOOLEAN, t.lineno(1), find_column(input_, t.slice[1]))
    
def p_primitive_nothing(t):
    'expression : TYPE_NOTHING'
    t[0] = Primitive(str(t[1]), Type.NULL, t.lineno(1), find_column(input_, t.slice[1]))    
             
def p_error(t):
    print("Syntactic error in '%s'" % t.value)

# ------------------------------ END GRAMMAR

input_ = ''

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    global input_
    input_ = input
    return parser.parse(input_)