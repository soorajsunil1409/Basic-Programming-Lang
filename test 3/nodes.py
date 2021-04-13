class NumberNode:
    def __init__(self, node):
        self.node = node

        self.pos_start = node.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"{self.node}"

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
