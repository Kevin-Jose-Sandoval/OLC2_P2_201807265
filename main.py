from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
arr = [1,2,3,4,5,6];
for i in [1,2,3,4,5,6]
    println(arr[i] == 1, arr[i] == 2, arr[i] == 3, arr[i] == 4, arr[i] == 5, arr[i] == 6);
end;

println("=================================FOR-3=================================");
for e in [1,2,3,4,5,6]
    if(length(arr) > e)
        println(e*arr[e],e*arr[e],e*arr[e],e*arr[e],e*arr[e],e*arr[e]);
    end;
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