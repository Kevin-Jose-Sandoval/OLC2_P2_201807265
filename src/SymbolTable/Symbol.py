class Symbol:
    def __init__(self, id_, type_, position_, is_global_, in_heap_):
        self.id = id_
        self.type = type_
        self.value = None
        
        self.pos = position_
        self.isGlobal = is_global_
        self.inHeap = in_heap_
        
        self.type_array = None
        self.type_struct = None