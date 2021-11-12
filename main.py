from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
array = [
        [12,9,4,99,56,34,78,22,1,3,10,13,120],
        [32,7*3,7,89,56,909,109,2,9,9874^0,44,3,820*10,11,8*0+8,10],
        [2,3,4,5],
        1
    ]::Vector{Vector{Int64}};



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