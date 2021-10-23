from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
    #a=(55+3)/(3-3);
    #println(2^3);
    #println((55+3)/(3-3));
    #println(uppercase("aa AA kevin Jose SANDOVAL"));
    
    #println("hola" * "mundo" * "HOLA" * "2018");
    println("holaM"^3);
    println("Terminó");
    
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
