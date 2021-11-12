from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
val1 = 1::Int64;
val2 = 10::Int64;
val3 = 2021.2020::Float64;

println("Probando declaracion de variables");
println(val1, " ", val2, " ", val3);
println("---------------------------------");
# COMENTARIO DE UNA LINEA
val1 = val1 + 41 - 123 * 4 / (2 + 2 * 2) - (10 + (125 % 5)) * 2 ^ 2;
val2 = 11 * (11 % (12 + -10)) + 22 / 2;
val3 = 2 ^ (2 * 12 / 6) + 25 / 5#= COMENTARIO
MULTILINEA =#;
println("Probando asignación de variables y aritmeticas");
println(val1, " ", val2, " ", val3);
println("---------------------------------");

rel1 = (((val1 - val2) == 24) && (true && (false || 5 >= 5))) || ((7*7) != (15+555) || -61 > 51);
rel2 = (7*7) <= (15+555) && 1 < 2;
rel3 = ((0 == 0) != ((532 > 532)) == ("Hola" == "Hola")) && (false || (false == true));
println("Probando relacionales y logicas");
println(rel1, " ", rel2, " ", rel3);
println("---------------------------------");

println("OPERACIONES " * "CON " * "Cadenas"^3);
despedida = "Adios mundo :c";
println(uppercase("Hola Mundo! ") * lowercase(despedida));

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
    print('----------------- SYMBOL TABLE ------------------')
    for i in generator.symbol_table:
        print(i.toString())
    print('----------------------------------------------')    
    
compile()