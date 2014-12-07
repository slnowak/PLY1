__author__ = 'novy'


class Symbol(object):

    def __init__(self, name, type):
        self.name, self.type = name, type


class VariableSymbol(Symbol):

    def __init__(self, name, type, value):
        super(VariableSymbol, self).__init__(name, type)
        self.value = value


class SymbolTable(object):

    def __init__(self, parent, name, type):
        self.parent, self.symbol, self.symbols = parent, Symbol(name, type), {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        return self.symbols[name]

    def get_parent_scope(self):
        return self.parent





