import re
from CompilationError import *
from enum import Enum
from derivatives import *
from Lex import SUPERSCRIPT_SYMBOLS
from Lex import SUBSCRIPT_SYMBOLS
import math




constant_pattern = re.compile("(-)?\d+(\.\d+)?")  # f(x) = c function pattern
one_degree_pattern = re.compile("(-)?(\d+(\.\d+)?)?(x|y|z)")  # f(x) = x function pattern
one_degree_expr_pattern = re.compile("(-)?(\d+(\.\d+)?)?\(.+\)")  # f(x) = c * g(x)
n_degree_pattern = re.compile("(-)?(\d+(\.\d+)?)?(x|y|z)\^(\d+(\.\d+)?)")  # f(x) = c * x^n function pattern
n_degree_expr_pattern = re.compile("(-)?(\d+(\.\d+)?)?\(.+\)\^(\d+(\.\d+)?)")  # f(x) = c * g(x)^n
sin_pattern = re.compile("(-)?(\d+(\.\d+)?)?sin\(.+\)")  # f(x) = c*sin(g(x)) function pattern
cos_pattern = re.compile("(-)?(\d+(\.\d+)?)?cos\(.+\)")  # f(x) = c*cos(g(x)) function pattern
tan_pattern = re.compile("(-)?(\d+(\.\d+)?)?tan\(.+\)")  # f(x) = c*tan(g(x)) function pattern
ln_pattern = re.compile("(-)?(\d+(\.\d+)?)?(ln|log)\(.+\)")  # f(x) = c*ln(g(x)) function pattern
exp_pattern = re.compile("(-)?(\d+(\.\d+)?)?\*(-)?(\d+(\.\d+)?)?\^\(.+\)")  # f(x) = c*a^(g(x))
sqrt_pattern = re.compile("(-)?(\d+(\.\d+)?)?sqrt\(.+\)")  # f(x) = c*sqrt(g(x))


class DerivativeSolver:

    def __init__(self, expression):
        self._expression = expression
        self._elements = list()
        self._differentiated_elements = list()
        self._expression = self._pad_with_pluses(self._expression)
        self._compile_exression()

    def derivative(self):
        return DerivativeSolver._to_string(self._differentiated_elements)


# some private methods

    def _compile_exression(self):
        terms = DerivativeSolver._tokenize(self._expression)
        self._elements = DerivativeSolver._parse_terms(terms)
        for i, element in enumerate(self._elements):
            dx_element = DerivativeSolver._differentiate(element)
            self._differentiated_elements.append(dx_element)

    @staticmethod
    def _parse_terms(terms):

        parsed = list()
        for term in terms:
            if constant_pattern.fullmatch(term):
                parsed.append((int(term), Function.POLY, 0, None))
            elif one_degree_pattern.fullmatch(term):
                coeff_str = term[:term.find("x")]
                if not coeff_str:
                    parsed.append((1, Function.POLY, 1, None))
                elif coeff_str == "-":
                    parsed.append((-1, Function.POLY, 1, None))
                else:
                    parsed.append((float(coeff_str), Function.POLY, 1, None))
            elif n_degree_pattern.fullmatch(term):
                coeff_str = term[:term.find("x")]
                deg_str = term[term.find("^") + 1:]
                if not coeff_str:
                    parsed.append((1, Function.POLY, float(deg_str), None))
                elif coeff_str == "-":
                    parsed.append((-1, Function.POLY, float(deg_str), None))
                else:
                    parsed.append((float(coeff_str), Function.POLY, float(deg_str), None))
            elif n_degree_expr_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.POLY, term)
                deg_str = term[term.find("^") + 1:]
                item[DEGREE] = float(deg_str)
                parsed.append(item)
            elif sin_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.SIN, term)
                parsed.append(item)
            elif cos_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.COS, term)
                parsed.append(item)
            elif tan_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.TAN, term)
                parsed.append(item)
            elif ln_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.LOG, term)
                parsed.append(item)
            elif sqrt_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.SQRT, term)
                parsed.append(item)
            elif exp_pattern.fullmatch(term):
                start_expr = term.find("(")
                end_expr = term.find(")")
                end_coeff = term.find("*")
                end_base = term.find("^")
                inner_func_str = term[start_expr + 1: end_expr].strip()
                if end_coeff == -1:  # the coeff is either 1 or -1
                    if term[0] == "-":
                        coeff = -1
                    else:
                        coeff = 1
                    base_str = term[:end_base]
                    return parsed.append((coeff, Function.EXP, abs(float(base_str)), inner_func_str))
                else:  # the coeff in neither -1 nor 1
                    coeff_str = term[:end_coeff]
                    base_str = term[end_coeff + 1, end_base]
                    return parsed.append((float(coeff_str), Function.EXP, float(base_str), inner_func_str))
            elif one_degree_expr_pattern.fullmatch(term):
                item = DerivativeSolver._parse_term(Function.POLY, term)
                item[DEGREE] = 1
                parsed.append(item)
            else:  # product of functions or quotient of functions
                find_div = term.find("/")
                find_mult = term.find("*")
                if not find_div == -1:
                    first_term, second_term = term[:find_div], term[find_div + 1]
                    parsed_first_term = DerivativeSolver._parse_terms(first_term)
                    parsed_second_term = DerivativeSolver._parse_terms(second_term)
                    parsed.append((1, Function.DIV, 1, [parsed_first_term, parsed_second_term]))
                elif not find_mult == -1:
                    first_term, second_term = term[:find_mult], term[find_mult + 1]
                    parsed_first_term = DerivativeSolver._parse_terms(first_term)
                    parsed_second_term = DerivativeSolver._parse_terms(second_term)
                    parsed.append((1, Function.MULT, 1, [parsed_first_term, parsed_second_term]))
                else:  # invalid expression
                    raise CompilationError("Invalid expression") 

        return parsed

    @staticmethod
    def _parse_term(func_type, term):
        start_expr = term.find("(")
        end_expr = term.find(")")
        inner_func_str = term[start_expr + 1: end_expr].strip()
        inner_func_str = DerivativeSolver._pad_with_pluses(inner_func_str)
        inner_func_tokenized = DerivativeSolver._tokenize(inner_func_str)
        inner_func_terms = DerivativeSolver._parse_terms(inner_func_tokenized)
        coeff_str = term[:term.find(derivatives_strings[func_type])]
        if not coeff_str:
            return 1, func_type, 1, inner_func_terms  #  we change the degree later, in parse terms func, where necessary
        elif coeff_str == "-":
            return -1, func_type, 1, inner_func_terms
        else:
            return float(coeff_str), func_type, None, inner_func_terms

    @staticmethod
    def _differentiate(term):
        # term is a 4-tuple
        if term[FUNCTION_TYPE] == Function.MULT:
            first_term_der = DerivativeSolver._differentiate(term[INNER_FUNCTION][FIRST])
            second_term_der = DerivativeSolver._differentiate(term[INNER_FUNCTION][SECOND])
            res_first_term = (1, Function.MULT, 1, [first_term_der, term[INNER_FUNCTION][SECOND]])
            res_second_term = (1, Function.MULT, 1, [second_term_der, term[INNER_FUNCTION][FIRST]])
            return [res_first_term, res_second_term]

        elif term[FUNCTION_TYPE] == Function.DIV:
            first_term_der = DerivativeSolver._differentiate(term[INNER_FUNCTION][FIRST])
            second_term_der = DerivativeSolver._differentiate(term[INNER_FUNCTION][SECOND])
            res_first_term = (1, Function.MULT, 1, [first_term_der, term[INNER_FUNCTION][SECOND]])
            res_second_term = (-1, Function.MULT, 1, [second_term_der, term[INNER_FUNCTION][FIRST]])
            denominator_term = (1, Function.POLY, 2, term[INNER_FUNCTION][SECOND])
            nominator_term = [res_first_term, res_second_term]
            return 1, Function.DIV, 1, [nominator_term, denominator_term]

        else:  # chain rule
            outer_function_der = derivatives[term[FUNCTION_TYPE]](term)
            if term[INNER_FUNCTION] is not None:
                inner_function_der = list()
                for term in term[INNER_FUNCTION]:
                    inner_function_der.append(DerivativeSolver._differentiate(term[INNER_FUNCTION]))
                return 1, Function.MULT, 1, [outer_function_der, inner_function_der]
            return outer_function_der

    @staticmethod
    def _group_elements(terms):

        for i, term in enumerate(terms):
            if term[FUNCTION_TYPE] == Function.MULT:
                outer, inner = term[INNER_FUNCTION]
                if inner[FUNCTION_TYPE] == Function.POLY and inner[DEGREE] == 0:
                    terms[i] = (outer[COEFF] * inner[COEFF], outer[FUNCTION_TYPE], outer[DEGREE], outer[INNER_FUNCTION])
                elif outer[FUNCTION_TYPE] == Function.POLY and outer[DEGREE] == 0:
                    terms[i] = (inner[COEFF] * outer[COEFF], inner[FUNCTION_TYPE], inner[DEGREE], inner[INNER_FUNCTION])

    @staticmethod
    def _to_string(terms):
        text = str()
        for i, term in enumerate(terms):
            if term[COEFF] == -1:
                text += "-"
            elif term[COEFF] == 0:
                continue
            elif term[COEFF] != 1:
                if term[COEFF] > 0:
                    text += "+"
                text += str(term[COEFF])

            if term[FUNCTION_TYPE] == Function.MULT:
                outer, inner = term[INNER_FUNCTION]
                if inner[FUNCTION_TYPE] == Function.POLY: # TODO bug here to fix
                    text += "(" + DerivativeSolver._to_string(inner) + ")" + DerivativeSolver._to_string(outer)
                else:
                    text += DerivativeSolver._to_string(inner) + DerivativeSolver._to_string(outer)
            elif term[FUNCTION_TYPE] == Function.DIV:
                nominator, denominator = term[INNER_FUNCTION]
                if nominator[FUNCTION_TYPE] == Function.POLY:
                    text += "(" + DerivativeSolver._to_string(nominator) + ")"
                else:  # no need for parentheses for non-polynomial function
                    text += DerivativeSolver._to_string(nominator)
                text += "/"
                if denominator[FUNCTION_TYPE] == Function.POLY:
                    text += "(" + DerivativeSolver._to_string(denominator) + ")"
                else:  # no need for parentheses for non-polynomial function
                    text += DerivativeSolver._to_string(denominator)
            elif term[FUNCTION_TYPE] == Function.POLY:
                if term[INNER_FUNCTION] is None:
                    if term[DEGREE] > 0:
                        text += "x"
                    if term[DEGREE] > 1:
                        text += "^" + str(term[DEGREE])
                else:
                    if term[DEGREE] > 0:
                        text += "(" + DerivativeSolver._to_string(term[INNER_FUNCTION]) + ")"
                    if term[DEGREE] > 1:
                        text += "^" + str(term[DEGREE])
            elif term[FUNCTION_TYPE] == Function.SIN:
                text += "sin(" + DerivativeSolver._to_string(term[INNER_FUNCTION]) + ")"
            elif term[FUNCTION_TYPE] == Function.COS:
                text += "cos(" + DerivativeSolver._to_string(term[INNER_FUNCTION]) + ")"
            elif term[FUNCTION_TYPE] == Function.TAN:
                text += "tan(" + DerivativeSolver._to_string(term[INNER_FUNCTION]) + ")"
            elif term[FUNCTION_TYPE] == Function.EXP:
                if term[COEFF] != 1:
                    text += "*"
                text += "e^(" + str(term[INNER_FUNCTION]) + ")"
            elif term[FUNCTION_TYPE] == Function.LOG:
                text += "log(" + DerivativeSolver._to_string(term[INNER_FUNCTION]) + ")"
            elif term[FUNCTION_TYPE] == Function.SQRT:
                text += "\u221A" + "(" + DerivativeSolver._to_string(term[INNER_FUNCTION]) + ")"
        return text


    @staticmethod
    def _pad_with_pluses(expression):
        chars = list(expression)
        new_chars = list()
        for c in chars:
            if c == "-":
                new_chars.append("+")
            new_chars.append(c)
        return "".join(new_chars)

    @staticmethod
    def _tokenize(expression):

        elements = list()
        stack = list()
        start, end = 0, len(expression)
        for i, symbol in enumerate(expression):
            if symbol == "(":
                stack.append(0)
            elif symbol == ")":
                stack.pop()
            elif symbol == "+" and (not stack):
                elements.append(expression[start: i].strip())
                start = i + 1

        if not stack:
            elements.append(expression[start: end].strip())

        return elements




