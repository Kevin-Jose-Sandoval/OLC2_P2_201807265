from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
    a = 100;
for letra in "Hola Mundo!"
    println(letra);
end;
 
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