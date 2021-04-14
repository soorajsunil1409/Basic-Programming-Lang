class NumberNode:
    def __init__(self, node):
        self.node = node

        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"{self.node}"

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
