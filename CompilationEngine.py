from Tokenizer import *
from Operators import *
# THERE MUST BE AN ADVANCE AT THE END OF EVERY COMPILE FUNCTION
# THE ASSUMPTION THAN THERE IS AN ADVANCE BEFORE COMPILE CALL


class CompilationEngine:

    def __init__(self, expression):
        self._expression = expression
        self.tokenizer = Tokenizer(expression)
        self.elements = list()  # operands and operators

    def run(self):
        print("Original: " + self._expression)
        self.tokenizer.advance()
        self.compile_expression()
        print(self.elements)
        postfix = self.to_postfix()
        print(postfix)
        res = self.evaluate_postfix(postfix)
        return res

    def compile_expression(self):
        """
        the funciton compiles the expression and converts to infix
        notation, evaluating the functions like sqrt, sin, cos
        """
        self.compile_term()
        while self.tokenizer.token_type() == SYMBOL and \
                (self.tokenizer.symbol() not in EXRESSION_TERMINATION) and \
                self.tokenizer.has_more_tokens():

            if self.tokenizer.token_type() == SYMBOL and (self.tokenizer.symbol() in OP):
                self.elements.append(self.tokenizer.symbol())
            else:  # an error
                raise CompilationError(INVALID_TOKEN)
            self.tokenizer.advance()
            self.compile_term()
        if self.tokenizer.token_type() == SYMBOL:
            self.elements.append(")")  # if the loop exited from ")" symbol, then add it to the expr

    def compile_term(self):

        cur_token = str()
        cur_type = self.tokenizer.token_type()
        if cur_type == SYMBOL:
            cur_token = self.tokenizer.symbol()
        elif cur_type == KEYWORD:
            cur_token = self.tokenizer.keyword()
        elif cur_type == IDENTIFIER:
            cur_token = self.tokenizer.identifier()
        elif cur_type == INT_CONST:
            cur_token = self.tokenizer.int_value()
        elif cur_type == FLOAT_CONST:
            cur_token = self.tokenizer.float_value()
        elif cur_type == STRING_CONST:
            cur_token = self.tokenizer.string_value()
        else:  # an error
            raise CompilationError(INVALID_TOKEN)
        self.tokenizer.advance()

        if cur_type == INT_CONST:
            self.elements.append(int(cur_token))
        elif cur_type == FLOAT_CONST:
            if cur_token == "e" or cur_token == "pi":
                self.elements.append(operators[cur_token])
            else:
                self.elements.append(float(cur_token))
        elif cur_type == IDENTIFIER:  # function name
            if self.tokenizer.token_type() == SYMBOL and self.tokenizer.symbol() == "(":
                self.elements.append("(")  # adding extra pair of parenteses
                self.elements.append(cur_token)
                self.elements.append("(")
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance()
                self.elements.append(")")  # adding extra pair of parenteses

        elif cur_type == SYMBOL:
            if cur_token == "-":
                self.elements.append("(")
                self.elements.append("~")
                self.elements.append("(")
                self.compile_term()
                self.elements.append(")")
                self.elements.append(")")
            elif cur_token == "!":
                self.elements.append("(")
                self.elements.append("!")
                self.elements.append("(")
                self.compile_term()
                self.elements.append(")")
                self.elements.append(")")

            elif cur_token == "(":
                self.elements.append(cur_token)
                self.compile_expression()
                self.tokenizer.advance()
            else:
                raise CompilationError(INVALID_TOKEN)
        else:  # an error
            raise CompilationError(INVALID_TOKEN)

    def to_postfix(self):
        postfix = list()
        stack = list()
        for i in range(len(self.elements)):
            if isinstance(self.elements[i], int) or \
               isinstance(self.elements[i], float):
                postfix.append(self.elements[i])
            elif self.elements[i] == "(":
                stack.append(self.elements[i])
            elif self.elements[i] == ")":
                while len(stack) != 0 and stack[-1] != "(":
                    postfix.append(stack.pop())
                stack.pop()
            else:  # term is an operator
                if len(stack) == 0 or stack[-1] == "(":
                    stack.append(self.elements[i])
                else:
                    while len(stack) != 0 and stack[-1] != "(" and \
                         self._precedence(self.elements[i]) <= self._precedence(stack[-1]):
                        postfix.append(stack.pop())
                    stack.append(self.elements[i])
        while len(stack):
            postfix.append(stack.pop())

        return postfix

    @staticmethod
    def _precedence(element):
        if element == "^":
            return 3
        elif element == "*" or element == "/":
            return 2
        elif element == "+" or element == "-":
            return 1

    @staticmethod
    def evaluate_postfix(postfix):
        stack = list()
        for i in range(len(postfix)):
            if isinstance(postfix[i], int) or \
               isinstance(postfix[i], float):
                stack.append(postfix[i])
            elif postfix[i] == "e" or postfix[i] == "pi":
                stack.append(operators[postfix[i]])
            else:
                if postfix[i] in UNARY_OP:
                    item = stack.pop()
                    item = operators[postfix[i]](item)
                    stack.append(item)
                else:
                    a = stack.pop()
                    b = stack.pop()
                    res = operators[postfix[i]](b, a)
                    stack.append(res)

        return stack.pop()





