import re
from Lex import *
from CompilationError import *
NO_TOKENS = "NO TOKENS"


class Tokenizer:

    def __init__(self, expression):

        expression = self._move_factorial(expression)
        self.terminals = list()
        expression = self._remove_whitespace(expression)
        self._tokenize(expression)
        self.current_token = str()

    def has_more_tokens(self):
        return len(self.terminals) > 0

    def advance(self):
        if self.has_more_tokens():
            self.current_token = self.terminals.pop(0)
        else:  # an error
            self.current_token = (None, None)

    def token_type(self):
        return self.current_token[1]

    def keyword(self):
        if self.token_type() == KEYWORD:
            return self.current_token[0]
        return None

    def symbol(self):
        if self.token_type() == SYMBOL:
            return self.current_token[0]
        return None

    def identifier(self):
        if self.token_type() == IDENTIFIER:
            return self.current_token[0]
        return None

    def int_value(self):
        if self.token_type() == INT_CONST:
            return self.current_token[0]
        return None

    def float_value(self):
        if self.token_type() == FLOAT_CONST:
            return self.current_token[0]
        return None

    def string_value(self):
        if self.token_type() == STRING_CONST:
            return self.current_token[0]
        return None

# Some private functions, should not be called outside
    @staticmethod
    def _move_factorial(expression):
        stack = list()
        index = expression.find("!")
        after = index + 1
        if index != -1:
            index -= 1
            if expression[index] == ")":
                stack.append(expression[index])
            if not len(stack):
                return expression[:index] + "!" + expression[index] + expression[after:]
            index -= 1
            while index >= -1:
                if expression[index] == "(":
                    stack.pop()
                if not len(stack):
                    return expression[:index] + "!" + expression[index:after - 1] + expression[after:]
                index -= 1
        return expression

    @staticmethod
    def _remove_whitespace(expression):
        return re.sub("\s", "", expression)

    def _tokenize(self, expression):
        # the basic idea is to to take a line
        # and make a list out of it where every
        # character is an element, then we put
        # spaces around the SYMBOLS and join
        # all the characters together. finally
        # we split the string using the regex \s+
        # and we get a tokenized line and put it
        # to the terminals list

        expr_chars = list(expression)
        for i in range(len(expr_chars)):
            if expr_chars[i] in SYMBOLS:
                expr_chars[i] = " " + expr_chars[i] + " "
        expression = "".join(expr_chars).strip()
        elements = list()

        elements.extend(re.split("\s+", expression))
        for element in elements:
            if element in SYMBOLS:
                self.terminals.append((element, SYMBOL))
            elif self._isint(element):
                self.terminals.append((element, INT_CONST))
            elif self._isfloat(element):
                self.terminals.append((element, FLOAT_CONST))
            else:
                self.terminals.append((element, IDENTIFIER))

    @staticmethod
    def _isfloat(x):
        if x == "e" or x == "pi":  # special float constants
            return True
        try:
            a = float(x)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def _isint(x):
        try:
            a = float(x)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b

