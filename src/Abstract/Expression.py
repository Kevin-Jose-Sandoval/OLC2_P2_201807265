from abc import ABC, abstractmethod

class Expression(ABC):    
    def __init__(self, line_, column_):
        self.line = line_
        self.column = column_
        self.true_label = ''
        self.false_label = ''
        super().__init__()
        
    @abstractmethod
    def compile(self, environment_):
        pass