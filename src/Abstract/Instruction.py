from abc import ABC, abstractmethod

class Instruction(ABC):    
    def __init__(self, line_, column_):
        self.line = line_
        self.column = column_
        super().__init__()
        
    @abstractmethod
    def compile(self, environment_):
        pass