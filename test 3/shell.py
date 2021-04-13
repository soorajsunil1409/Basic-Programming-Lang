from lexer import Lexer
from parser import Parser
from nodes import *
from values import *
from interpreter import *

global_symbol_table = Symbol_Table()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("true", Number(1))
global_symbol_table.set("false", Number(0))

def run(text):
    lexer = Lexer(text, "<stdin>")
    tokens, error = lexer.get_tokens()

    # return tokens, None
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    # return ast.node, None
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    if result.error: return None, result.error

    return result.value, None


while True:
    text = input(">>> ")
    result, error = run(text)
    if error: print(error)
    else: print(result)