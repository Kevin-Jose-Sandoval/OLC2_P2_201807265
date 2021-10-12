class Value:
    def __init__(self, value_, type_, is_temp, aux_type = ""):
        self.value = value_
        self.type = type_
        self.is_temp = is_temp
        self.aux_type = aux_type
        self.true_label = ''
        self.false_label = ''