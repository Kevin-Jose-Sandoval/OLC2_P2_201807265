from src.Generator.Generator3D import Generator
from flask import Flask, request
from flask_cors import CORS

from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *
from src.SymbolTable.Types import *

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<h1>COMPILADORES 2 - PROYECTO 2</h1>"

@app.route("/compile", methods=['POST'])
def compile():
    input_ = request.json['input']
    
    generator_aux = Generator()
    generator_aux.cleanAll()
    generator = generator_aux.getInstance()
    
    new_env = Environment(None)
    new_env.scope = SymbolTableType.GLOBAL    

    ast = parse(input_)    
    try:
        for instr in ast:
            instr.compile(new_env)
    except:
        print("Error al compilar instrucciones")
        
    key = 0;
    for i in generator.symbol_table:
        key += 1
        type_ = i.type
        scope_ = i.scope
        if isinstance(i.type, SymbolTableType): type_ = i.type.name
        if isinstance(i.scope, SymbolTableType): scope_ = i.scope.name
        generator.table.append([key, i.name, type_, scope_])
    
    key = 0;
    for i in generator.errors:
        key += 1
        generator.aux_errors.append([key, i.message, i.line, i.column])
        
    return { 'msg': generator.getCode(), 'code': 200 }

@app.route("/symbol-table", methods=['GET'])
def getSymbolTable():
    generator_aux = Generator()
    generator = generator_aux.getInstance() 
       
    return { 'msg': generator.table, 'code': 200 }

@app.route("/errors", methods=['GET'])
def getErrors():
    generator_aux = Generator()
    generator = generator_aux.getInstance() 
        
    return { 'msg': generator.aux_errors, 'code': 200 }

if __name__ == "__main__":
    app.run()