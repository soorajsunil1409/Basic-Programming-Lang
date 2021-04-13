from str_with_arrows import *

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f"  File {self.pos_start.fn}, line {self.pos_end.ln + 1}"
        result += "\n    " + str_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        result += f"\n{self.error_name}: {self.details}\n"
        return result

class IllegalCharacterException(Error):
    def __init__(self, pos_start, pos_end, deatils):
        super().__init__(pos_start, pos_end, "Illegal Character", deatils)

class InvalidSyntaxException(Error):
    def __init__(self, pos_start, pos_end, deatils):
        super().__init__(pos_start, pos_end, "Invalid Syntax", deatils)

class ExpectedCharacterException(Error):
    def __init__(self, pos_start, pos_end, deatils):
        super().__init__(pos_start, pos_end, "Expected Character", deatils)

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def __str__(self):
        result = self.generate_traceback()
        result += "\n    " + str_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        result += f"\n{self.error_name}: {self.details}\n"
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f"  File \"{pos.fn}\", line {pos.ln + 1}, in {ctx.display_name}\n"
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result 
