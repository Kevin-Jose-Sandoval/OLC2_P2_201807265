from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
a = 10;
while a > 0
    print("El valor de a es: ");
    println(a);
    a = a - 1;
end;
println("--");
while a < 5
    a = a + 1;
    if a == 3
        println("a");
        continue;
    elseif a == 4
        println("b");
        break;
    end;
    print("El valor de a es: ");
    println(a);
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
    
compile()
