# imports
# general
from src.SymbolTable.Types import *
from src.SymbolTable.Exception import *

# instructions
from src.Instruction.Statement import *
from src.Instruction.Print import *
from src.Instruction.Variables.Declaration import *
from src.Instruction.Conditional.If import *
from src.Instruction.Loops.While import *
from src.Instruction.Loops.Break import *
from src.Instruction.Loops.Continue import *
from src.Instruction.Functions.Function import *
from src.Instruction.Functions.Param import *
from src.Instruction.Functions.Return import *
from src.Instruction.Loops.For import *
from src.Instruction.Arrays.Array import *
from src.Instruction.Arrays.AssignArray import *

# expressions
from src.Expression.Arithmetic import *
from src.Expression.Primitive import *
from src.Expression.Relational import *
from src.Expression.Logical import *
from src.Expression.Access import *
from src.Natives.UpperCase import *
from src.Natives.LowerCase import *
from src.Expression.CallFunction import *
from src.Natives.DataManagement import *
from src.Expression.WayIterate import *
from src.Expression.CallArray import *
from src.Natives.Length import *

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
    'uppercase' : 'UPPER',
    'lowercase' : 'LOWER',
    
    # native data management
    'parse'     : 'PARSE',
    'trunc'     : 'TRUNC',
    'float'     : 'FLOAT',
    'string'    : 'STRING',
    'typeof'    : 'TYPE_OF',
    
    # natives arrays
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
                | declaration_st SEMICOLON
                | if_st SEMICOLON
                
                | while_st SEMICOLON
                | for_st SEMICOLON
                | break_st SEMICOLON
                | continue_st SEMICOLON
                
                | declare_function_st SEMICOLON
                | call_function_st SEMICOLON
                | return_st SEMICOLON
                
                | call_array_st SEMICOLON
                | assign_array_st SEMICOLON
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
    #errors.append(Exception("En la instruccion: " + str(t[1].value), t.lineno(1), find_column(input_, t.slice[1])))
    t[0] = ""
    
# ------------------------------ PRINT
def p_println_st(t):
    'print_st : PRINTLN LEFT_PAR expression_list RIGHT_PAR'
    t[0] = Print(t[3], t.lineno(1), find_column(input_, t.slice[1]), True)

def p_print_st(t):
    'print_st : PRINT LEFT_PAR expression_list RIGHT_PAR'
    t[0] = Print(t[3], t.lineno(1), find_column(input_, t.slice[1]))

def p_println_none(t):
    'print_st : PRINTLN LEFT_PAR RIGHT_PAR'
    t[0] = Print(None, t.lineno(1), find_column(input_, t.slice[1]), True)

def p_print_none(t):
    'print_st : PRINT LEFT_PAR RIGHT_PAR'
    t[0] = Print(None, t.lineno(1), find_column(input_, t.slice[1]))
    
# ------------------------------ DECLARATION
def p_declaration_st(t):
    '''
    declaration_st : ID EQUAL expression
    '''
    if len(t) == 4:
        t[0] = Declaration(t[1], t[3], t.lineno(2), find_column(input_, t.slice[2]))

# ------------------------------ ACCESS ID
def p_expression_id(t):
    'expression : ID'
    t[0] = Access(t[1], t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ IF
def p_if_st(t):
    '''
    if_st : IF expression statement END
          | IF expression statement ELSE statement END
          | IF expression statement else_if_list END
    '''
    if len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]))
    elif len(t) == 7:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]), t[5])
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]), t[4])
                
def p_else_if_list(t):
    '''
    else_if_list : ELSE_IF expression statement
                 | ELSE_IF expression statement ELSE statement
                 | ELSE_IF expression statement else_if_list
    '''
    if len(t) == 4:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]), t[5])
    elif len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]), t[4])

# ------------------------------ WHILE
def p_while_st(t):
    'while_st : WHILE expression statement END'
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ FOR
def p_for_st(t):
    # for ID in ways_iterate
    '''
    for_st : FOR ID IN ways_iterate statement END
    '''
    t[0] = For(t[2], t[4], t[5], t.lineno(1), find_column(input_, t.slice[1]))

def p_for_rank(t):
    # 4 : 5
    'ways_iterate : expression COLON expression'
    t[0] = WayIterate(t[1], t[3], TypeIteration.RANK, t.lineno(1), 0)

def p_for_string(t):
    'ways_iterate : PRIMITIVE_STRING'
    t[0] = WayIterate(t[1], None, TypeIteration.STRING, t.lineno(1), 0)
    
def p_for_ID(t):
    'ways_iterate : ID'
    t[0] = WayIterate(t[1], None, TypeIteration.ID, t.lineno(1), 0)

def p_for_direct_array(t):
    'ways_iterate : LEFT_BRACKET expression_list RIGHT_BRACKET'
    t[0] = WayIterate(t[2], None, TypeIteration.ARRAY, t.lineno(1), 0)

# ------------------------------ BREAK
def p_break_st(t):
    'break_st : BREAK'
    t[0] = Break(t.lineno(1), find_column(input_, t.slice[1]))
            
# ------------------------------ CONTINUE
def p_continue_st(t):
    'continue_st : CONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ FUNCTIONS
def p_declaration_function_st(t):
    '''
    declare_function_st : FUNCTION ID LEFT_PAR RIGHT_PAR COLON COLON type statement END
                        | FUNCTION ID LEFT_PAR declare_params RIGHT_PAR COLON COLON type statement END
    '''
    if len(t) == 10:
        t[0] = Function(t[2], [], t[7], t[8], t.lineno(1), find_column(input_, t.slice[1]))
    else:
        t[0] = Function(t[2], t[4], t[8], t[9], t.lineno(1), find_column(input_, t.slice[1]))

def p_declaration_function_void(t):
    '''
    declare_function_st : FUNCTION ID LEFT_PAR RIGHT_PAR statement END
                        | FUNCTION ID LEFT_PAR declare_params RIGHT_PAR statement END
    '''
    if len(t) == 7:
        t[0] = Function(t[2], [], None, t[5], t.lineno(1), find_column(input_, t.slice[1]))
    else:
        t[0] = Function(t[2], t[4], None, t[6], t.lineno(1), find_column(input_, t.slice[1]))

def p_declare_params(t):
    '''
    declare_params : declare_params COMMA ID COLON COLON type
                   | ID COLON COLON type
    '''
    if len(t) == 5:
        t[0] = [Param(t[1], t[4], t.lineno(1), find_column(input_, t.slice[1]))]
    else:
        t[1].append(Param(t[3], t[6], t.lineno(3), t.lexpos(3)))
        t[0] = t[1]

# ------------------------------ FUNCTION - CALL FUNCTION
def p_call_function_st(t):
    '''
    call_function_st : ID LEFT_PAR RIGHT_PAR
                     | ID LEFT_PAR expression_list RIGHT_PAR
    '''
    if len(t) == 4:
        t[0] = CallFunction(t[1], [], t.lineno(1), find_column(input_, t.slice[1]))
    else:
        t[0] = CallFunction(t[1], t[3], t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ ARRAYS
#  DECLARATION ARRAY
def p_expression_array(t):
    'expression : LEFT_BRACKET expression_list RIGHT_BRACKET'
    t[0] = Array(t[2], t.lineno(1), find_column(input_, t.slice[1]), len(t[2]))
    
# ACCESS ARRAY
def p_expression_call_array(t):
    # ID dimension_list
    'call_array_st : ID dimension_list'
    t[0] = CallArray(t[1], t[2], t.lineno(1), find_column(input_, t.slice[1]))

def p_array_dimension_list(t):
    # [expression][expression][expression]...
    '''
    dimension_list : dimension_list position
                   | position
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_position(t):
    '''
    position : LEFT_BRACKET expression RIGHT_BRACKET
    '''
    t[0] = t[2]

# ------------------------------ ACCESS EXPRESSION (FUNCTION, ARRAY, NATIVE_ARRAY)
def p_expression_access(t):
    '''
    expression : call_function_st
               | call_array_st
               | native_array_st
    '''
    t[0] = t[1]

# ------------------------------ ASSIGN ARRAY
def p_assign_array_st(t):
    'assign_array_st : ID dimension_list EQUAL expression'
    t[0] = AssignArray(t[1], t[2], t[4], t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ RETURN
def p_return_st(t):
    '''
    return_st : RETURN
              | RETURN expression
    '''
    if len(t) == 2:
        t[0] = Return(None, t.lineno(1), find_column(input_, t.slice[1]))
    else:
        t[0] = Return(t[2], t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ TYPES
def p_type(t):
    '''
    type : TYPE_INT64
         | TYPE_FLOAT64
         | TYPE_BOOL
         | TYPE_CHAR
         | TYPE_STRING
         | TYPE_NOTHING         
    '''

    if t[1] == 'Int64':
        t[0] = Type.INT64
    elif t[1] == 'Float64':
        t[0] = Type.FLOAT64
    elif t[1] == 'Bool':
        t[0] = Type.BOOLEAN
    elif t[1] == 'Char':
        t[0] = Type.CHAR
    elif t[1] == 'String':
        t[0] = Type.STRING
    elif t[1] == 'Nothing':
        t[0] = Type.NULL                

# ------------------------------ LIST EXPRESSIONS
def p_expression_list(t):
    '''
    expression_list : expression_list COMMA expression
                    | expression
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

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
        t[0] = Arithmetic(Primitive(0, Type.INT64, t.lineno(1), find_column(input_, t.slice[1])),
                          t[2], ArithmeticType.MINUS, t.lineno(1), find_column(input_, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logical(t[2], None, LogicalType.NOT, t.lineno(1), find_column(input_, t.slice[1]))

# ------------------------------ EXPRESSIONS - NATIVE ARRAY
def p_native_array_st(t):
    '''
    native_array_st : LENGTH LEFT_PAR ID RIGHT_PAR
    '''
    t[0] = Length(t[3], t.lineno(1), find_column(input_, t.slice[1])) 

# ------------------------------ NATIVES
def p_expression_uppercase(t):
    'expression : UPPER LEFT_PAR expression RIGHT_PAR'
    t[0] = UpperCase(t[3], t.lineno(1), find_column(input_, t.slice[1]))

def p_expression_lowercase(t):
    'expression : LOWER LEFT_PAR expression RIGHT_PAR'
    t[0] = LowerCase(t[3], t.lineno(1), find_column(input_, t.slice[1]))

def p_expression_trunc(t):
    'expression : TRUNC LEFT_PAR expression RIGHT_PAR'
    t[0] = DataManagement(TypeNative.TRUNC, t[3], t.lineno(1), find_column(input_, t.slice[1]))

def p_expression_float(t):
    'expression : FLOAT LEFT_PAR expression RIGHT_PAR'
    t[0] = DataManagement(TypeNative.FLOAT, t[3], t.lineno(1), find_column(input_, t.slice[1]))

def p_expression_string(t):
    'expression : STRING LEFT_PAR expression RIGHT_PAR'
    t[0] = DataManagement(TypeNative.STRING, t[3], t.lineno(1), find_column(input_, t.slice[1]))

def p_expression_parse_string(t):
    'expression : PARSE LEFT_PAR type COMMA expression RIGHT_PAR'
    t[0] = DataManagement(TypeNative.PARSE, t[5], t.lineno(1), find_column(input_, t.slice[1]), t[3])

# ------------------------------ EXPRESSIONS - PRIMITIVES
def p_primitive_int(t):
    'expression : PRIMITIVE_INT'
    t[0] = Primitive(int(t[1]), Type.INT64, t.lineno(1), find_column(input_, t.slice[1]))

def p_primitive_float(t):
    'expression : PRIMITIVE_FLOAT'
    t[0] = Primitive(float(t[1]), Type.FLOAT64, t.lineno(1), find_column(input_, t.slice[1]))

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