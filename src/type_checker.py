__author__ = 'novy'

from src.symbol_table import SymbolTable, VariableSymbol


ttype = {}
arithmetic_operators = ['+', '-', '*', '/', '%']
bitwise_operators = ['|', '&', '^', '<<', '>>']
logical_operators = ['&&', '||']
comparison_operators = ['==', '!=', '>', '<', '<=', '>=']
assignment_operators = ['=']


def all_operators():
    return arithmetic_operators + bitwise_operators + logical_operators + assignment_operators + comparison_operators


for operator in all_operators():
    ttype[operator] = {}
    for type_ in ['int', 'float', 'string']:
        ttype[operator][type_] = {}

for arithmetic_operator in arithmetic_operators:
    ttype[arithmetic_operator]['int']['int'] = 'int'
    ttype[arithmetic_operator]['int']['float'] = 'float'
    ttype[arithmetic_operator]['float']['int'] = 'float'
    ttype[arithmetic_operator]['float']['float'] = 'float'
ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'
ttype['=']['float']['int'] = 'float'
ttype['=']['float']['float'] = 'float'
ttype['=']['int']['int'] = 'int'
ttype['=']['string']['string'] = 'string'

for operator in bitwise_operators + logical_operators:
    ttype[operator]['int']['int'] = 'int'

for comp_op in comparison_operators:
    ttype[comp_op]['int']['int'] = 'int'
    ttype[comp_op]['int']['float'] = 'int'
    ttype[comp_op]['float']['int'] = 'int'
    ttype[comp_op]['float']['float'] = 'int'
    ttype[comp_op]['string']['string'] = 'int'


class TypeChecker(object):
    def dispatch(self, node, *args):
        self.node = node
        classname = node.__class__.__name__
        method = getattr(self, 'visit_' + classname)
        return method(node, *args)

    def findVariable(self, tab, variable):
        if variable in tab.symbols:
            return tab.get(variable)
        elif tab.symbol.name == variable:
            return tab.symbol
        elif tab.get_parent_scope() is not None:
            return self.findVariable(tab.get_parent_scope(), variable)

        return None

    def visit_Program(self, node):
        tab = SymbolTable(None, "program", None)
        self.dispatch(node.declarations, tab)
        self.dispatch(node.fundefs, tab)
        self.dispatch(node.instructions, tab)

    def visit_Declarations(self, node, tab):
        for declaration in node.declarations:
            self.dispatch(declaration, tab)

    def visit_Declaration(self, node, tab):
        self.dispatch(node.inits, tab, node.type)

    def visit_Inits(self, node, tab, type):
        for init in node.inits:
            self.dispatch(init, tab, type)

    def visit_Init(self, node, tab, type):
        if node.id in tab.symbols:
            print "Duplicated usage of symbol {0} in line {1}".format(node.id, node.line - 1)

        value_type = self.dispatch(node.expression, tab)
        if not type == value_type:
            print "Value of type {0} cannot be assigned to symbol {1} of type {2} (line {3})" \
                .format(value_type, node.id, type, node.line - 1)
        else:
            tab.put(node.id, VariableSymbol(node.id, type, node.expression))

    def visit_Instructions(self, node, tab):
        for instruction in node.instructions:
            self.dispatch(instruction, tab)

    def visit_Instruction(self, node, tab):
        pass

    def visit_Print(self, node, tab):
        self.dispatch(node.expression, tab)

    def visit_Labeled(self, node, tab):
        self.dispatch(node.instruction, tab)

    def visit_Assignment(self, node, tab):
        variable = self.findVariable(tab, node.id)
        if variable is None:
            print "Symbol {0} in line {1} not defined before".format(node.id, node.line - 1)
        else:
            value_type = self.dispatch(node.expression, tab)
            if not value_type in ttype["="][variable.type]:
                print "Value of type {0} cannot be assigned to symbol {1} of type {2} (line {3})" \
                    .format(value_type, node.id, variable.type, node.line - 1)
            else:
                return ttype["="][variable.type][value_type]

    def visit_Choice(self, node, tab):
        self.dispatch(node._if, tab)
        self.dispatch(node._if, tab)

    def visit_If(self, node, tab):
        self.dispatch(node.cond, tab)
        self.dispatch(node.statement, tab)

    def visit_Else(self, node, tab):
        self.dispatch(node.statement, tab)

    def visit_While(self, node, tab):
        self.dispatch(node.cond, tab)
        self.dispatch(node.statement, tab)

    def visit_RepeatUntil(self, node, tab):
        self.dispatch(node.cond, tab)
        self.dispatch(node.statement, tab)

    def visit_Return(self, node, tab):
        self.dispatch(node.expression, tab)

    def visit_Continue(self, node, tab):
        pass

    def visit_Break(self, node, tab):
        pass

    def visit_Compound(self, node, tab, *args):
        if len(args) > 0 and args[0] is True:
            self.dispatch(node.declarations, tab)
            self.dispatch(node.instructions, tab)
        else:
            new_tab = SymbolTable(tab, None, None)
            self.dispatch(node.declarations, new_tab)
            self.dispatch(node.instructions, new_tab)

    def visit_Condition(self, node, tab):
        pass

    def visit_Expression(self, node, tab):
        pass

    def visit_Const(self, node, tab):
        value = node.value
        if (value[0] in ('"', "'")) and (value[len(value) - 1] in ('"', "'")):
            return 'string'
        try:
            int(value)
            return 'int'
        except ValueError:
            try:
                float(value)
                return 'float'
            except ValueError:
                print "Value's {0} type is not recognized".format(value)

    def visit_Id(self, node, tab):
        variable = self.findVariable(tab, node.id)
        if variable is None:
            print "Symbol {0} in line {1} not declared before".format(node.id, node.line)
        else:
            return variable.type

    def visit_BinExpr(self, node, tab):
        type1 = self.dispatch(node.expr1, tab)
        type2 = self.dispatch(node.expr2, tab)
        operator = node.operator

        if type1 is None or not type2 in ttype[operator][type1]:
            print "Incompatible types in line", node.line
        else:
            return ttype[operator][type1][type2]

    def visit_ExpressionInParentheses(self, node, tab):
        expression = node.expression
        return self.dispatch(expression, tab)

    def visit_IdWithParentheses(self, node, tab):
        variable = self.findVariable(tab, node.id)
        if variable is None:
            print "Symbol {0} in line {1} not declared before".format(node.id, node.line)
        else:
            self.dispatch(node.expression_list, tab)
            return variable.type

    def visit_ExpressionList(self, node, tab):
        for expression in node.expressions:
            self.dispatch(expression, tab)

    def visit_FunctionDefinitions(self, node, tab):
        for fundef in node.fundefs:
            self.dispatch(fundef, tab)

    def visit_FunctionDefinition(self, node, tab):
        new_tab = SymbolTable(tab, node.id, node.type)
        self.dispatch(node.arglist, new_tab)
        self.dispatch(node.compound_instr, new_tab, True)

    def visit_ArgumentList(self, node, tab):
        for arg in node.arg_list:
            self.dispatch(arg, tab)

    def visit_Argument(self, node, tab):
        if node.id in tab.symbols:
                print "Duplicated usage of symbol {0} in line {1}".format(node.id, node.line - 1)
        else:
            tab.put(node.id, VariableSymbol(node.id, node.type, None))
            return node.type

