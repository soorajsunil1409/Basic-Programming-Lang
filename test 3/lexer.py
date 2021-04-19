from tokens import Tokens, TokenTypes
from exceptions import *
from string import ascii_letters

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
LETTERS = ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
KEYWORDS = [
    "var",
    "and",
    "or",
    "not",
    "if",
    "elif",
    "else",
    "for",
    "to",
    "while",
    "step",
    "def"
]

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
            elif self.current_char in LETTERS + "_":
                tokens.append(self.make_identifier())
            elif self.current_char == "+":
                tokens.append(self.make_plus())
            elif self.current_char == "-":
                tokens.append(self.make_arrow_minus())
            elif self.current_char == "/":
                tokens.append(self.make_div())
            elif self.current_char == "^":
                tokens.append(Tokens(TokenTypes.POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(self.make_mul())
            elif self.current_char == "(":
                tokens.append(Tokens(TokenTypes.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Tokens(TokenTypes.RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ",":
                tokens.append(Tokens(TokenTypes.COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == "$":
                tokens.append(Tokens(TokenTypes.DOLLAR, pos_start=self.pos))
                self.advance()
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == "|":
                tokens.append(Tokens(TokenTypes.PIPE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "\"":
                self.make_string()
            elif self.current_char == "=":
                token = self.make_equals()
                tokens.append(token)
            elif self.current_char == "<":
                token = self.make_less_than()
                tokens.append(token)
            elif self.current_char == ">":
                token = self.make_greater_than()
                tokens.append(token)
            else:
                pos_start = self.pos.get_pos()
                char = self.current_char
                return [], IllegalCharacterException(pos_start, self.pos, "\"%s\"" % char)

        tokens.append(Tokens(TokenTypes.EOF, pos_start=self.pos))
        return tokens, None

    def make_plus(self):
        tok_type = TokenTypes.PLUS
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.PLUSE

        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_mul(self):
        tok_type = TokenTypes.MUL
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.MULE

        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_div(self):
        tok_type = TokenTypes.DIVIDE
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.DIVE

        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_arrow_minus(self):
        tok_type = TokenTypes.MINUS
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == ">":
            self.advance()
            tok_type = TokenTypes.ARROW

        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Tokens(TokenTypes.NE, pos_start=pos_start, pos_end=self.pos), None
        elif self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.MINUSE
        
        self.advance()
        return None, ExpectedCharacterException(
            pos_start, self.pos,
            '"=" (after "!")'
        )

    def make_equals(self):
        tok_type = TokenTypes.EQ
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.EE

        self.advance()
        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TokenTypes.LT
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.LTE


        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TokenTypes.GT
        pos_start = self.pos.get_pos()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TokenTypes.GTE

        return Tokens(tok_type, pos_start=pos_start, pos_end=self.pos)

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

        if num_str.startswith("."):
            num_str = "0" + num_str
        elif num_str.endswith("."):
            num_str += "0"

        return Tokens(TokenTypes.FLOAT, float(num_str), pos_start, self.pos) if "." in num_str else Tokens(TokenTypes.INT, int(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.get_pos()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TokenTypes.KEYWORD if id_str in KEYWORDS else TokenTypes.IDENTIFIER

        return Tokens(tok_type, id_str, pos_start, self.pos)
