from lexer import Lexer
from parser import Parser
from nodes import *
from interpreter import *
from math import pi

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_float = BuiltInFunction("is_float")
BuiltInFunction.is_int = BuiltInFunction("is_int")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_bool = BuiltInFunction("is_bool")
BuiltInFunction.is_func = BuiltInFunction("is_func")
BuiltInFunction.clear = BuiltInFunction("clear")

global_symbol_table = Symbol_Table()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("PI", Number(pi))

global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("is_string", BuiltInFunction.is_string)
global_symbol_table.set("is_number", BuiltInFunction.is_number)
global_symbol_table.set("is_float", BuiltInFunction.is_float)
global_symbol_table.set("is_int", BuiltInFunction.is_int)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_bool", BuiltInFunction.is_bool)
global_symbol_table.set("is_func", BuiltInFunction.is_func)
global_symbol_table.set("clear", BuiltInFunction.clear)

def run(text):
    lexer = Lexer(text, "<stdin>")
    tokens, error = lexer.get_tokens()

    # return tokens, None
    if error: return None, error
    if len(tokens) == 1: return None, None

    parser = Parser(tokens)
    ast = parser.parse()

    # return ast.node, None
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


while True:
    text = input(">>> ")
    result, error = run(text)
    if error: print(error)
    elif result: print(repr(result))