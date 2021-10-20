from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *
from src.SymbolTable.Generator import *

def compile():
    input_ = '''
    println(5^0);
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
