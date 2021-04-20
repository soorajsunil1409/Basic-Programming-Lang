from lexer import Lexer
from parser import Parser
from nodes import *
from interpreter import *

global_symbol_table = Symbol_Table()
global_symbol_table.set("null", Number(0))

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