from tokens import TokenTypes
from exceptions import InvalidSyntaxException
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens): 
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TokenTypes.EOF:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end, 
                'Expected "+", "-", "*", "==", "^", ">=", ">", "<=", "<", "and", "or", "not" or "/"'
                ))
        return res

    def expr(self):
        res = ParseResult()

        if self.current_tok.type == TokenTypes.DOLLAR:
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenTypes.IDENTIFIER:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected \"$\""
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenTypes.EQ:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected \"=\""
                ))
            
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TokenTypes.KEYWORD, "and"), (TokenTypes.KEYWORD, "or"))))

        if res.error:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected int, float, identifier, "$", "+", "-", "(", if, for, while, def or "not"'
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TokenTypes.KEYWORD, "not"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TokenTypes.EE, TokenTypes.NE, TokenTypes.LT, TokenTypes.LTE, TokenTypes.GT, TokenTypes.GTE)))
        if res.error: 
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected int, float, identifier, "+", "-", "(", or "not"'
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TokenTypes.PLUS, TokenTypes.MINUS))

    def term(self):
        return self.bin_op(self.factor, (TokenTypes.MUL, TokenTypes.DIVIDE))
        
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenTypes.PLUS, TokenTypes.MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.power()

    def power(self):
        return self.bin_op(self.call, (TokenTypes.POW, ), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TokenTypes.LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TokenTypes.RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error: 
                    return res.failure(InvalidSyntaxException(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        'Expected ")", "$", "if", "for", "while", "def", int, float, identifier, "+", "-", "(" or not',
                    ))
                
                while self.current_tok.type == TokenTypes.COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res 

                if self.current_tok.type != TokenTypes.RPAREN:
                    return res.failure(InvalidSyntaxException(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        'Expected "," or ")"'
                    ))
                
                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenTypes.FLOAT, TokenTypes.INT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TokenTypes.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TokenTypes.LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TokenTypes.RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected \")\""
                ))

        elif tok.matches(TokenTypes.KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        
        elif tok.matches(TokenTypes.KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)
        
        elif tok.matches(TokenTypes.KEYWORD, "while"):
            for_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TokenTypes.KEYWORD, "def"):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxException(
            self.current_tok.pos_start, self.current_tok.pos_end,
            'Expected int, float, identifier, "+", "-", "(", if, for, while, def'
        ))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TokenTypes.KEYWORD, "def"):
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "def"'
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenTypes.IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TokenTypes.LPAREN:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected "("'
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TokenTypes.LPAREN:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected identifier or "("'
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TokenTypes.IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TokenTypes.COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TokenTypes.IDENTIFIER:
                    return res.failure(InvalidSyntaxException(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        'Expected identifier'
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TokenTypes.RPAREN:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected ")" or ","'
                ))
        else:
            if self.current_tok.type != TokenTypes.RPAREN:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected identifier or ")"'
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenTypes.ARROW:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "->"'
            ))
        
        res.register_advancement()
        self.advance()

        node_to_return = res.register(self.expr())
        if res.error: return res

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TokenTypes.KEYWORD, "for"):
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected \"for\""
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenTypes.IDENTIFIER:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected \"identifier\""
            ))

        var_name = self.current_tok

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenTypes.LPAREN:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected \"(\""
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TokenTypes.COMMA:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected \",\""
            ))
        
        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type == TokenTypes.COMMA:
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if self.current_tok.type != TokenTypes.RPAREN:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected \")\""
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenTypes.PIPE:
            if step_value:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected \"|\""
                ))
            else:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected \"|\" or \"step\""
                ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TokenTypes.PIPE:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "|"'
            ))

        res.register_advancement()
        self.advance()

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TokenTypes.KEYWORD, "while"):
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "while"'
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TokenTypes.PIPE:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "|"'
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TokenTypes.PIPE:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "|"'
            ))

        res.register_advancement()
        self.advance()

        return res.success(WhileNode(condition, body))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TokenTypes.KEYWORD, "if"):
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "if"'
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TokenTypes.ARROW:
            return res.failure(InvalidSyntaxException(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected "->"'
            ))
        
        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res

        cases.append((condition, expr))

        while self.current_tok.matches(TokenTypes.KEYWORD, "elif"):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type != TokenTypes.ARROW:
                return res.failure(InvalidSyntaxException(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected "->"'
                ))
            
            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res

            cases.append((condition, expr))

        if self.current_tok.matches(TokenTypes.KEYWORD, "else"):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error: return res

        return res.success(IfNode(cases, else_case))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
