from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
    a = "pa";
    c = "hola";
    
    b = [ 10,25, [ 50, 60, [80] ], [ [100,200,[5000, 10000] ] ] ];
    println(b[3][3][1]);
    println(b[4][1][3][2]);
    
    #print(b[3][2]);    
    '''
    
    generator_aux = Generator()
    generator_aux.cleanAll()
    generator = generator_aux.getInstance()
    
    new_env = Environment(None)
    ast = parse(input_)

    for instruction in ast:
        instruction.compile(new_env)
        
    print(generator.getCode())
    
compile()
