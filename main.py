from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
struct Actor
    nombre:: String;
    edad:: Int64;
end;

struct Pelicula 
    nombre::String;
    posicion::Int64;
end;

struct Contrato
    actor::Actor;
    pelicula::Pelicula;
end;

actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];

function contratar(actor::Actor, pelicula::Pelicula)
    return Contrato(actor,pelicula);
end;

function crearActor(nombre::String, edad::Int64)
    return Actor(nombre,edad);
end;

function crearPelicula(nombre::String, posicion::Int64) 
    return Pelicula(nombre,posicion);
end;

function imprimir(contrato::Contrato)
    println("Actor: ", contrato.actor.nombre, "   Edad: ", contrato.actor.edad);
    println("Pelicula: ", contrato.pelicula.nombre, "   Genero: ", contrato.pelicula.posicion);
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