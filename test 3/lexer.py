from tokens import Tokens, TokenTypes
from exceptions import IllegalCharacterException

####################################
# POSITION CLASS
####################################

class Position:
        def __init__(self, idx, ln, col, fn, ftxt):
                self.idx = idx
                self.ln = ln
                self.col = col
                self.fn = fn
                self.ftxt = ftxt

        def advance(self, current_char=None):
                self.idx += 1
                self.col += 1

                if current_char == '\n':
                        self.ln += 1
                        self.col = 0

                return self

        def get_pos(self):
                return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

####################################
# LEXER CLASS
####################################

DIGITS = "1234567890"

class Lexer:
    def __init__(self, text, fn):
        self.text = text
        self.current_char = None
        self.pos = Position(-1, 0, -1, fn, text)
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def get_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t\n":
                self.advance()
            elif self.current_char in DIGITS + ".":
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Tokens(TokenTypes.PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Tokens(TokenTypes.MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Tokens(TokenTypes.DIVIDE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Tokens(TokenTypes.MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Tokens(TokenTypes.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Tokens(TokenTypes.RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.get_pos()
                char = self.current_char
                return [], IllegalCharacterException(pos_start, self.pos, "\"%s\"" % char)

        tokens.append(Tokens(TokenTypes.EOF, pos_start=self.pos))
        return tokens, None


    def make_number(self):
        num_str = ""
        dots_count = 0
        pos_start = self.pos.get_pos()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == "." and "." not in num_str:
                dots_count += 1
                if dots_count > 1:
                    break

            num_str += self.current_char
            self.advance()

        return Tokens(TokenTypes.FLOAT, float(num_str), pos_start, self.pos) if "." in num_str else Tokens(TokenTypes.INT, int(num_str), pos_start, self.pos)
