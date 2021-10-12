# Add C3D
class Generator:
    generator = None
    
    def __init__(self):
        # counters
        self.count_temp = 0
        self.count_label = 0
        # code
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        # temporary list
        self.temps = []
        # natives list
        self.printString = False

    # ============ Code 3D
    def initialHeader(self):
        header = '/*----- HEADER -----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'

        if len(self.temps) > 0:
            header += 'var '
            
            for i in range(len(self.temps)):
                header += self.temps[i]
                if i != (len(self.temps) - 1):
                    header += ', '
            
            header += ' float64;\n'
        
        header += 'var P, H float64;\nvar stack [26082000]float64;\nvar heap [26082000]float64;\n\n'
        return header
    
    def getCode(self):
        return f'{self.initialHeader()}{self.natives}\n{self.funcs}\n/*----- MAIN -----*/\nfunc main(){{\n{self.code}}}'
    
    def codeIn(self, code_, tab_ = "\t"):
        if self.inNatives:
            if self.natives == '':
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + tab_ + code_
            
        elif self.inFunc:
            if self.funcs == '':
                self.funcs = self.funcs + '/*-----FUNCS-----*/\n'
            self.funcs = self.funcs + tab_ +  code_
            
        else:
            self.code = self.code + '\t' +  code_    
    # ============ Auxiliary functions
    def addComment(self, comment_):
        self.codeIn(f'/* {comment_} */\n')
        
    def addSpace(self):
        self.codeIn("\n")
        
    def getInstance(self):
        if Generator.generator == None:
            Generator.generator = Generator()
        return Generator.generator
    
    def cleanAll(self):
        # counters
        self.count_temp = 0
        self.count_label = 0
        # Code
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        # temporary list
        self.temps = []
        # natives list
        self.printString = False
        Generator.generator = Generator()    
    
    # ============ Temporary - label - goto - expression - if
    def addTemp(self):
        temp = f't{self.count_temp}'
        self.count_temp += 1
        self.temps.append(temp)
        return temp

    def newLabel(self):
        label = f'L{self.count_label}'
        self.count_label += 1
        return label

    def addGoto(self, label_):
        self.codeIn(f'goto {label_};\n')    
    
    def putLabel(self, label_):
        self.codeIn(f'{label_}:\n')

    def addIf(self, left_, right_, operation_, label_):
        self.codeIn(f'if {left_} {operation_} {right_} {{goto {label_};}}\n')
                
    def addExpression(self, result_, left_, right_, operation_):
        self.codeIn(f'{result_}={left_}{operation_}{right_};\n')

    def addBeginFunc(self, id_):
        if not self.inNatives:
            self.inFunc = True
        self.codeIn(f'func {id_}(){{\n', '')

    def addEndFunc(self):
        self.codeIn('return;\n}\n');
        if not self.inNatives:
            self.inFunc = False
          
    # ============ INSTRUCTIONS
    def addPrint(self, type_, value_):
        self.codeIn(f'fmt.Printf("%{type_}", int({value_}));\n')
        
    def printTrue(self):
        self.addPrint("c", 116)
        self.addPrint("c", 114)
        self.addPrint("c", 117)
        self.addPrint("c", 101)

    def printFalse(self):
        self.addPrint("c", 102)
        self.addPrint("c", 97)
        self.addPrint("c", 108)
        self.addPrint("c", 115)
        self.addPrint("c", 101)

    # ============ STACK
    def setStack(self, pos_, value_):
        # stack[int(pos_)] = value_
        self.codeIn(f'stack[int({pos_})]={value_};\n')
    
    def getStack(self, place_, pos_):
        # place_ = stack[int(pos_)]
        self.codeIn(f'{place_}=stack[int({pos_})];\n')

    # ============ HEAP
    def setHeap(self, pos_, value_):
        # heap[int(pos_)] = value_
        self.codeIn(f'heap[int({pos_})]={value_};\n')

    def getHeap(self, place_, pos_):
        # place_ = heap[int(pos_)]        
        self.codeIn(f'{place_}=heap[int({pos_})];\n')

    def nextHeap(self):
        self.codeIn('H=H+1;\n')

    # ============ ENVIRONMENT
    def newEnv(self, size_):
        self.codeIn(f'P=P+{size_};\n')

    def callFun(self, id_):
        self.codeIn(f'{id_}();\n')

    def retEnv(self, size_):
        self.codeIn(f'P=P-{size_};\n')

    # ============ NATIVES  
    def fPrintString(self):
        if self.printString:
            return
        self.printString = True
        self.inNatives = True

        self.addBeginFunc('printString')
        # Label para salir de la funcion
        returnLbl = self.newLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.newLabel()

        # Temporal puntero a Stack
        tempP = self.addTemp()

        # Temporal puntero a Heap
        tempH = self.addTemp()

        self.addExpression(tempP, 'P', '1', '+')

        self.getStack(tempH, tempP)

        # Temporal para comparar
        tempC = self.addTemp()

        self.putLabel(compareLbl)

        self.getHeap(tempC, tempH)

        self.addIf(tempC, '-1', '==', returnLbl)

        self.addPrint('c', tempC)

        self.addExpression(tempH, tempH, '1', '+')

        self.addGoto(compareLbl)

        self.putLabel(returnLbl)
        self.addEndFunc()
        self.inNatives = False
