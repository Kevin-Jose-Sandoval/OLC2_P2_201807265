from src.Generator.Generator3D import Generator
from src.Grammar.grammar import parse
from src.SymbolTable.Environment import *

def compile():
    input_ = '''
function quicksort(array::Vector{Int64},low::Int64,n::Int64)::Int64
	lo = low::Int64;
	hi = n::Int64;
	if lo >= n
		return 0;
    end;
	mid = array[(trunc(((lo + hi) / 2)))]::Int64;
	while lo < hi
		while (lo<hi && array[lo] < mid)
			lo = lo + 1;
        end;
		while (lo<hi && array[hi] > mid)
			hi = hi - 1;
        end;
		if lo < hi
			T = array[lo]::Int64;
			array[lo] = array[hi];
			array[hi] = T;
        end;
    end;
	if (hi < lo)
		T = hi::Int64;
		hi = lo;
		lo = T;
    end;
	quicksort(array,low,lo);
	cond = 0::Int64;
	if ( lo == low)
		cond = lo + 1;
	else
		cond = lo;
    end;
	quicksort(array,cond,n);
end;
i = 0::Int64;
array = [
        [12,9,4,99,56,34,78,22,1,3,10,13,120],
        [32,7*3,7,89,56,909,109,2,9,9874^0,44,3,820*10,11,8*0+8,10]
    ]::Vector{Vector{Int64}};
    
    
println("Quick Sort");
println("Valores antes de Quicksort");
for x in 1:length(array[1])
	print(array[1][x]);
    print(", ");
 
end;
println("");
println("-------------------------");
quicksort(array[1],1,length(array[1]));
println("Valores despues de QuickSort:");
for y in 1:length(array[1])
	print(array[1][y]);
    print(", ");
 
end;
println("");
println("Valores antes de Quicksort");
for x in 1:length(array[2])
	print(array[2][x]);
    print(", ");
 
end;
println("");
println("-------------------------");
quicksort(array[2],1,length(array[2]));
println("Valores despues de QuickSort:");
for y in 1:length(array[2])
	print(array[2][y]);
    print(", ");
end;
println("-------------------------");

println(array[1][13]);
println(array[1][14]);
println(array[1][15]);
println(array[1][1]);
println(array[1][0]);



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