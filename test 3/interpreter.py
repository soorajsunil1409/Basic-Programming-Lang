from values import *
from tokens import TokenTypes

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.parent = parent
        self.display_name = display_name
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class Symbol_Table:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]


class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node, context)

    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.node.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        node_a = res.register(self.visit(node.node_a, context))
        if res.error: return res
        node_b = res.register(self.visit(node.node_b, context))
        if res.error: return res
        
        if node.bin_op.type == TokenTypes.PLUS:
            result, error = node_a.added_to(node_b)
        elif node.bin_op.type == TokenTypes.MINUS:
            result, error = node_a.subbed_by(node_b)
        elif node.bin_op.type == TokenTypes.MUL:
            result, error = node_a.multed_by(node_b)
        elif node.bin_op.type == TokenTypes.DIVIDE:
            result, error = node_a.divided_by(node_b)
        elif node.bin_op.type == TokenTypes.POW:
            result, error = node_a.powed_by(node_b)

        if error: 
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

        return result

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f'"{var_name}" is not defined',
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.factor, context))
        if res.error: return res

        error = None
        
        if node.op.type == TokenTypes.MINUS:
            result, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

class RTResult:
    def __init__(self):
        self.error = None
        self.value = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self
