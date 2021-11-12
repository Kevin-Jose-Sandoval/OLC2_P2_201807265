from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
# Struct Inmutable
struct Personaje
    nombre::String;
    edad::Int64;
    descripcion::String;
end;
# Struct Mutable
mutable struct Carro
    placa::String;
    color::String;
    tipo::String;
end;
# Construcción Struct
p1 = Personaje("Fer", 18, "No hace nada");
p2 = Personaje("Fer", 18, "Maneja un carro");
c1 = Carro("090PLO", "gris", "mecanico");
c2 = Carro("P0S921", "verde", "automatico");

# Asignación Atributos
p1.edad = 10; # Error, Struct Inmutable
p2.edad = 20; # Error, Struct Inmutable
c1.color = "cafe"; # Cambio aceptado
c2.color = "rojo"; # Cambio aceptado
# Acceso Atributo
println(p1.edad); # Imprime 18
println(c1.color); # Imprime cafe





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