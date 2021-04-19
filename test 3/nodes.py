class NumberNode:
    def __init__(self, node):
        self.node = node

        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"{self.node}"

class StringNode:
    def __init__(self, value):
        self.value = value

        self.pos_start = value.pos_start
        self.pos_end = value.pos_end

    def __repr__(self):
        return f"{self.value}"

class ListNode:
    def __init__(self, values):
        self.values = values

        self.pos_start = values[0].pos_start
        self.pos_end = values[-1].pos_end

    def __repr__(self):
        return f"{self.values}"

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class BinOpNode:
    def __init__(self, node_a, bin_op, node_b):
        self.node_a = node_a
        self.bin_op = bin_op
        self.node_b = node_b

        self.pos_start = self.node_a.pos_start
        self.pos_end = self.node_b.pos_end

    def __repr__(self):
        return f"({self.node_a}, {self.bin_op}, {self.node_b})"

class UnaryOpNode:
    def __init__(self, op, factor):
        self.op = op
        self.factor = factor

        self.pos_start = self.op.pos_start
        self.pos_end = self.factor.pos_end

    def __repr__(self):
        return f"({self.op}, {self.factor})"

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end

class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
