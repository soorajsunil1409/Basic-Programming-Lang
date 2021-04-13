from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context

def main(text):
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
    result = interpreter.visit(ast.node, context)

    if result.error: return None, result.error

    return result.value, None


while True:
    text = input(">>> ")
    result, error = main(text)
    if error: print(error)
    else: print(result)