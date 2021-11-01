from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
a = "pa";
b = [ "aa", "bb", "cc",["hh", "zz"] ];

println(b[4][2]);
b[4][2] = "holaMundo";
println(b[4][2]);



#println(b[3][3][1]);
#println(b[1+1+1][2+1+5][1]);
    '''
    
    generator_aux = Generator()
    generator_aux.cleanAll()
    generator = generator_aux.getInstance()
    
    new_env = Environment(None)
    ast = parse(input_)

    for instruction in ast:
        instruction.compile(new_env)
        
    print(generator.getCode())
    
    print('----------------- EXCEPTIONS ------------------')
    for i in generator.errors:
        print(i.toString())
    print('----------------------------------------------')
    
compile()