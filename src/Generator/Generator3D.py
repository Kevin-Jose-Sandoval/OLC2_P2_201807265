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
        self.potency = False
        self.upperCase = False
        self.lowerCase = False
        self.concatenateStr = False

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
        
        header += 'var P, H float64;\nvar stack [1000000]float64;\nvar heap [1000000]float64;\n\n'
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
        self.potency = False
        self.upperCase = False
        self.lowerCase = False        
        self.concatenate = False
        
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

    def printMathError(self):
        self.addPrint("c", 77)      # M
        self.addPrint("c", 97)      # a
        self.addPrint("c", 116)     # t
        self.addPrint("c", 104)     # h
        self.addPrint("c", 69)      # E
        self.addPrint("c", 114)     # r
        self.addPrint("c", 114)     # r
        self.addPrint("c", 111)     # o
        self.addPrint("c", 114)     # r
        
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

    def fPotency(self):
        if self.potency:
            return
        self.potency = True
        self.inNatives = True
        
        self.addBeginFunc('potency')
        t0 = self.addTemp()
        self.addExpression(t0, 'P', '1', '+')
        
        t1 = self.addTemp()
        self.getStack(t1, t0)
        
        self.addExpression(t0, t0, '1', '+')
        
        t2 = self.addTemp()
        self.getStack(t2, t0)
        
        self.addExpression(t0, t1, '', '')

        L0 = self.newLabel()
        L1 = self.newLabel()
        L2 = self.newLabel()
        exit_label = self.newLabel()
        
        # if exponent is 0, return in stack 1
        self.addIf(t2, '0', '==', L2)            
        
        # else, continue
        self.putLabel(L0)
        
        self.addIf(t2, '1', '<=', L1)
        self.addExpression(t1, t1, t0, '*')
        self.addExpression(t2, t2, '1', '-')
        self.addGoto(L0)
        self.putLabel(L1)
        self.setStack('P', t1)        
        self.addGoto(exit_label)
        
        # label if exponent is 0
        self.putLabel(L2)
        self.setStack('P', 1)
        
        self.putLabel(exit_label)
        
        self.addEndFunc()                
        self.inNatives = False
        
    def fUpperCase(self):
        if self.upperCase:
            return
        self.upperCase = True
        self.inNatives = True

        self.addBeginFunc('upperCase')
        
        t1 = self.addTemp()
        self.addExpression(t1, 'H', '', '')
        t2 = self.addTemp()
        self.addExpression(t2, 'P', '1', '+')
        self.getStack(t2, t2)
        
        L0 = self.newLabel()        
        self.putLabel(L0)
        
        L2 = self.newLabel()        
        L1 = self.newLabel()
        
        t3 = self.addTemp()
        self.getHeap(t3, t2)
        
        self.addIf(t3, '-1', '==', L2)
        self.addIf(t3, '97', '<', L1)
        self.addIf(t3, '122', '>', L1)
        
        self.addExpression(t3, t3, '32', '-')
        
        self.putLabel(L1)
        self.setHeap('H', t3)
        self.nextHeap()
        self.addExpression(t2, t2, '1', '+')
        self.addGoto(L0)
        
        self.putLabel(L2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t1)

        self.addEndFunc()
        self.inNatives = False
        
    def fLowerCase(self):
        if self.lowerCase:
            return
        self.lowerCase = True
        self.inNatives = True

        self.addBeginFunc('lowerCase')
        
        # Start code
        t1 = self.addTemp()
        self.addExpression(t1, 'H', '', '')
        t2 = self.addTemp()
        self.addExpression(t2, 'P', '1', '+')
        self.getStack(t2, t2)
        
        L0 = self.newLabel()        
        self.putLabel(L0)
        
        L2 = self.newLabel()        
        L1 = self.newLabel()
        
        t3 = self.addTemp()
        self.getHeap(t3, t2)
        
        self.addIf(t3, '-1', '==', L2)
        self.addIf(t3, '65', '<', L1)
        self.addIf(t3, '90', '>', L1)
        
        self.addExpression(t3, t3, '32', '+')
        
        self.putLabel(L1)
        self.setHeap('H', t3)
        self.nextHeap()
        self.addExpression(t2, t2, '1', '+')
        self.addGoto(L0)
        
        self.putLabel(L2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t1)
        # end code        
        
        self.addEndFunc()
        self.inNatives = False
        
    def fConcatenateStr(self):
        if self.concatenateStr:
            return
        self.concatenateStr = True
        self.inNatives = True

        self.addBeginFunc('concatenateStr')
        
        # start code
        t2 = self.addTemp()
        t3 = self.addTemp()
        t5 = self.addTemp()
        t4 = self.addTemp()
        
        self.addExpression(t2, 'H', '', '')
        self.addExpression(t3, 'P', '1', '+')
        self.getStack(t5, t3)
        self.addExpression(t4, 'P', '2', '+')
        
        L1 = self.newLabel()
        L2 = self.newLabel()
        
        self.putLabel(L1)
        t6 = self.addTemp()
        self.getHeap(t6, t5)
        
        self.addIf(t6, '-1', '==', L2)
        self.setHeap('H', t6)
        self.nextHeap()
        self.addExpression(t5, t5, '1', '+')
        self.addGoto(L1)
        
        self.putLabel(L2)
        self.getStack(t5, t4)
        
        L0 = self.newLabel()        
        L3 = self.newLabel()
        self.putLabel(L3)
        self.getHeap(t6, t5)
        
        self.addIf(t6, '-1', '==', L0)
        self.setHeap('H', t6)
        self.nextHeap()
        self.addExpression(t5, t5, '1', '+')
        self.addGoto(L3)
        
        self.putLabel(L0)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t2)
        # end code
        
        self.addEndFunc()
        self.inNatives = False