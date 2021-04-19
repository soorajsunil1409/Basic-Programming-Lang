from enum import Enum

class Tokens:
    def __init__(self, type_, value = None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.get_pos()
            self.pos_end = self.pos_start.get_pos()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"

class TokenTypes(Enum):
    FLOAT       = "Float"
    INT         = "Int"
    KEYWORD     = "Keyword"
    IDENTIFIER  = "Identifier"
    
    PLUS        = "Plus"
    MINUS       = "Minus"
    DIVIDE      = "Divide"
    MUL         = "Mul"
    MULE        = "MulE"
    PLUSE       = "MulE"
    MINUSE      = "MinusE"
    DIVE        = "DivE"
    POW         = "Pow"
    
    EQ          = "Eq"
    EE          = "Ee"
    NE          = "Ne"
    GT          = "Gt"
    LT          = "Lt"
    GTE         = "Gte"
    LTE         = "Lte"
    
    LPAREN      = "LParen"
    RPAREN      = "RParen"
    EOF         = "EOF"

    ARROW       = "Arrow"
    PIPE        = "Pipe"
    COMMA       = "Comma"
    DOLLAR      = "Dollar"
