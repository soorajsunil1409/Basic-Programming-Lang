from tokens import TokenTypes
from exceptions import *

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def divided_by(self, other):
        return None, self.illegal_operation(other)
            
    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def copy(self):
        raise Exception("no copy method defined")

    def execute(self, args):
    	return RTResult().failure(self.illegal_operation())

    def is_true(self):
        return False

    def illegal_operation(self, other=None, message=f'Illegal operation'):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            message,
            self.context
        )

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def divided_by(self, other, context):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, "Division by zero", context)
            return Number(self.value / other.value).set_context(context), None
        else:
            return None, Value.illegal_operation(self, other)
            
    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
        	return Boolean("true" if (self.value == other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Boolean("true" if (self.value != other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Boolean("true" if (self.value < other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Boolean("true" if (self.value > other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Boolean("true" if (self.value <= other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Boolean("true" if (self.value >= other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        return Boolean(str(self.is_true() and other.is_true()).lower()), None

    def ored_by(self, other):
        return Boolean(str(self.is_true() or other.is_true()).lower()), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        self.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return f"{self.value}"

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Boolean("true" if (self.value == other.value) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, String):
            return Boolean("true" if (len(self.value) > len(other.value)) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, String):
            return Boolean("true" if (len(self.value) < len(other.value)) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, String):
            return Boolean("true" if (len(self.value) >= len(other.value)) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, String):
            return Boolean("true" if (len(self.value) <= len(other.value)) else "false").set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, String):
            return Boolean("true" if (self.value and other.value) else "false").set_context(self.context), None
        elif isinstance(other, Boolean):
            second = other.value.capitalize()
            return Boolean(str(self.is_true() and eval(second)).lower()), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, String):
            return Boolean("true" if (self.value or other.value) else "false").set_context(self.context), None
        elif isinstance(other, Boolean):
            second = other.value.capitalize()
            return Boolean(str(self.is_true() or eval(second)).lower()), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Boolean("false" if self.value else "true").set_context(self.context), None

    def is_true(self):
        return len(self.value) >  0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        self.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"

class List(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        new_list = self.copy()
        new_list.value.append(other.value)
        return new_list, None

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()

            new_list.value.extend(other.value)
            return new_list, None
        else:
            return None, Value.illegal_operation(other, message=f'Expected List type, instead got a {type(other).__name__} type')
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.value.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                other.pos_start, other.pos_end,
                'List index out of bounds',
                self.context
                )
        else:
            return None, Value.illegal_operation(other, message=f'Expected Number type, instead got a {type(other).__name__} type')

    def divided_by(self, other, context):
        if isinstance(other, Number):
            try:
                return self.value[other.value], None
            except:
                return None, RTError(
                other.pos_start, other.pos_end,
                'List index out of bounds',
                self.context
                )
        else:
            return None, Value.illegal_operation(other, message=f'Expected Number type, instead got a {type(other).__name__} type')

    def is_true(self):
        return self.value

    def copy(self):
        copy = List(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        self.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([f"{x}" for x in self.value])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.value])}]'

class Boolean(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def notted(self):
        return Boolean("false" if self.is_true() else "true"), None

    def anded_by(self, other):
        first = self.value.capitalize()
        if isinstance(other, Boolean):
            second = other.value.capitalize()
            return Boolean(str(eval(first) and eval(second)).lower()), None
        else:
            second = other.is_true()
            return Boolean(str(eval(first) and second).lower()), None

    def ored_by(self, other):
        first = self.value.capitalize()
        if isinstance(other, Boolean):
            second = other.value.capitalize()
            return Boolean(str(eval(first) or eval(second)).lower()), None
        else:
            second = other.is_true()
            return Boolean(str(eval(first) or second).lower()), None

    def is_true(self):
        return self.value == "true"

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        self.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = Symbol_Table(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))
        
        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)        

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.error: return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.error: return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error: return res
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

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

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.parent = parent
        self.display_name = display_name
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class Symbol_Table:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

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

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.value.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for elem in node.values:
            elements.append(res.register(self.visit(elem, context)))
        
        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.node.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BooleanNode(self, node, context):
        return RTResult().success(
            Boolean(node.value.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

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
            result, error = node_a.divided_by(node_b, context)
        elif node.bin_op.type == TokenTypes.POW:
            result, error = node_a.powed_by(node_b)
        elif node.bin_op.type == TokenTypes.EE:
            result, error = node_a.get_comparison_eq(node_b)
        elif node.bin_op.type == TokenTypes.NE:
            result, error = node_a.get_comparison_ne(node_b)
        elif node.bin_op.type == TokenTypes.LT:
            result, error = node_a.get_comparison_lt(node_b)
        elif node.bin_op.type == TokenTypes.GT:
        	result, error = node_a.get_comparison_gt(node_b)
        elif node.bin_op.type == TokenTypes.LTE:
        	result, error = node_a.get_comparison_lte(node_b)
        elif node.bin_op.type == TokenTypes.GTE:
        	result, error = node_a.get_comparison_gte(node_b)
        elif node.bin_op.matches(TokenTypes.KEYWORD, 'and'):
        	result, error = node_a.anded_by(node_b)
        elif node.bin_op.matches(TokenTypes.KEYWORD, 'or'):
        	result, error = node_a.ored_by(node_b)

        if error: 
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

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
        elif node.op.matches(TokenTypes.KEYWORD, "not"):
            result, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RTResult()

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error: return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value = Number(1)

        i = start_value.value

        # if start_value.value >= 0:
        if end_value.value > i:
            condition = lambda: i < end_value.value
        elif end_value.value < i:
            condition = lambda: i > end_value.value
        else:
            condition = lambda: i == end_value.value
        # else:
        #     condition = lambda: i > end_value.value
        #     print(condition(), 2)

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            res.register(self.visit(node.body_node, context))
            if res.error: return res
        
        return res.success(None)

    def visit_WhileNode(self, node, context):
        res = RTResult()

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true(): break

            res.register(self.visit(node.body_node, context))
            if res.error: return res
        
        return res.success(None)

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names)
        func_value.set_context(context)
        func_value.set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value) 

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
        
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)