import re
import numpy as np
from CompilationError import *
from Lex import SUPERSCRIPT_SYMBOLS
from Lex import SUBSCRIPT_SYMBOLS
COEFF = 0
DEGREE = 1
OPERATOR = 0


class EquationSolver:

    def __init__(self, expression):
        self._expression = expression
        self._elements = list()
        self._pad_with_pluses()
        self._compile_expression()
        self._max_deg = self._get_degree()
        self._group_elements()
        self._coeffs = self._get_coeeficients()

    def solve(self):
        roots = np.roots(np.array(self._coeffs))
        return roots

    def simplify(self):
        expr_str = str()
        for i, element in enumerate(self._elements):

            if element[COEFF] > 0 and i:
                expr_str += "+"
            if element[COEFF]:
                expr_str += str(element[COEFF])
                if element[DEGREE] > 0:
                    expr_str += "x"
                if element[DEGREE] > 1:
                    expr_str += self._to_superscript(element[DEGREE])
        return expr_str

# some private methods

    def _compile_expression(self):
        left_right_expressions = re.split("\s*=\s*", self._expression)
        left_expression = left_right_expressions[0]
        if len(left_right_expressions) == 1:
            right_expression = ""
        else:
            right_expression = left_right_expressions[1]

        tokenized_left_terms = self._tokenize(left_expression)
        tokenized_right_terms = self._tokenize(right_expression)
        parsed_left_terms = self._parse_terms(tokenized_left_terms)
        parsed_right_terms = self._parse_terms(tokenized_right_terms)
        postfix_left_terms = self._to_postfix(parsed_left_terms)
        postfix_right_terms = self._to_postfix(parsed_right_terms)
        left_terms = self._evaluate_postfix(postfix_left_terms)
        right_terms = self._evaluate_postfix(postfix_right_terms)
        self._elements.extend(left_terms)
        right_terms = list(map(lambda x: (-x[0], x[1]), right_terms))
        self._elements.extend(right_terms)

    def _get_coeeficients(self):
        return list(map(lambda x: x[COEFF], self._elements))

    def _get_degree(self):
        max_deg = 0
        for element in self._elements:
            if element[DEGREE] > max_deg:
                max_deg = element[DEGREE]

        return max_deg

    def _pad_with_pluses(self):
        chars = list(self._expression)
        new_chars = list()
        for c in chars:
            if c == "-":
                new_chars.append("+")
            new_chars.append(c)
        self._expression = "".join(new_chars)

    def _group_elements(self):
        grouped_elements = list()
        for i in range(self._max_deg, -1, -1):
            summ = 0
            for element in self._elements:
                if element[DEGREE] == i:
                    summ += element[COEFF]
            grouped_elements.append((summ, i))
        self._elements = grouped_elements

    def _to_postfix(self, terms):
        postfix = list()
        stack = list()
        for i, term in enumerate(terms):
            if term[DEGREE] > -1:
                postfix.append(term)
            elif term[OPERATOR] == "(":
                stack.append(term)
            elif term[OPERATOR] == ")":
                while len(stack) != 0 and stack[-1][OPERATOR] != "(":
                    postfix.append(stack.pop())
                stack.pop()
            else:  # elements[i] is an operator
                if len(stack) == 0 or stack[-1][OPERATOR] == "(":
                    stack.append(term)
                else:
                    while len(stack) != 0 and stack[-1][OPERATOR] != "(" and \
                         self._precedence(term) <= self._precedence(stack[-1]):
                        postfix.append(stack.pop())
                    stack.append(term)

        while len(stack):
            postfix.append(stack.pop())

        return postfix

    @staticmethod
    def _evaluate_postfix(postfix):
        stack = list()
        for i, term in enumerate(postfix):
            if term[DEGREE] > -1:
                stack.append([term])
            else:  # term is an operator
                res = list()
                a = stack.pop()
                b = stack.pop()
                if term[OPERATOR] == "*":
                    for k in a:
                        for j in b:
                            res.append((k[COEFF] * j[COEFF], k[DEGREE] + j[DEGREE]))
                if term[OPERATOR] == "+":
                    for k in a:
                        res.append(k)
                    for k in b:
                        res.append(k)
                stack.append(res)
        if stack:
            return stack.pop()
        else:
            return list()

    @staticmethod
    def _precedence(element):
        if element[OPERATOR] == "^":
            return 3
        elif element[OPERATOR] == "*" or element[OPERATOR] == "/":
            return 2
        elif element[OPERATOR] == "+" or element[OPERATOR] == "-":
            return 1

    @staticmethod
    def _tokenize(expression):
        symbols = ["+", "*", "/", "(", ")"]
        expr_chars = list(expression)
        for i in range(len(expr_chars)):
            if expr_chars[i] in symbols:
                expr_chars[i] = " " + expr_chars[i] + " "
        expression = "".join(expr_chars).strip()
        elements = list()

        elements.extend(re.split("\s+", expression))
        return elements

    @staticmethod
    def _parse_terms(terms):
        parsed = list()
        constant_pattern = re.compile("(-)?\d+(\.\d+)?")
        one_degree_pattern = re.compile("(-)?(\d+(\.\d+)?)?(x|y|z)")
        n_degree_pattern = re.compile("(-)?(\d+(\.\d+)?)?(x|y|z)\^\d+")

        for term in terms:
            if constant_pattern.fullmatch(term):
                parsed.append((int(term), 0))
            elif one_degree_pattern.fullmatch(term):
                coeff_str = term[:term.find("x")]
                if not coeff_str:
                    parsed.append((1, 1))
                elif coeff_str == "-":
                    parsed.append((-1, 1))
                else:
                    parsed.append((int(coeff_str), 1))
            elif n_degree_pattern.fullmatch(term):
                coeff_str = term[:term.find("x")]
                deg_str = term[term.find("^") + 1:]
                if not coeff_str:
                    parsed.append((1, int(deg_str)))
                elif coeff_str == "-":
                    parsed.append((-1, int(deg_str)))
                else:
                    parsed.append((int(coeff_str), int(deg_str)))

            elif term in ["+", "*", "/", "(", ")"]:
                parsed.append((term, -1))

            else:
                if term:
                    raise CompilationError("Invalid Token")

        return parsed

    def _to_superscript(self, num):
        sup = str()

        while num > 0:
            digit = num % 10
            sup = SUPERSCRIPT_SYMBOLS[digit] + sup
            num //= 10

        return sup


def format_result(roots):

    def _to_subscript(num):
        sup = str()

        while num > 0:
            digit = num % 10
            sup = SUBSCRIPT_SYMBOLS[digit] + sup
            num //= 10

        return sup


    roots = np.around(roots, 3)
    print("Original " + str(roots))
    formatted_roots = list()

    for item in roots:
        formatted_real = str()
        formatted_img = str()
        re = item.real
        im = item.imag
        if not im:
            if re == int(re):
                formatted_real = str(int(re))
            else:
                formatted_real = str(re)

        else:
            if re == int(re):
                formatted_real = str(int(re))
            else:
                formatted_real = str(re)
            if not re:
                formatted_real = str()

            if im == int(im):
                formatted_img = str(int(im)) + "i"
            else:
                formatted_img = str(im) + "i"

        if formatted_img:
            if formatted_real:
                formatted_roots.append(formatted_real + "+" + formatted_img)
            else:
                formatted_roots.append(formatted_img)
        else:
            formatted_roots.append(formatted_real)

    formatted_roots = list(set(formatted_roots))
    formatted_str = str()
    for i, root in enumerate(formatted_roots):
        formatted_str += "x" + _to_subscript(i + 1) + "=" + str(root) + ", "

    return formatted_str[:-2]




