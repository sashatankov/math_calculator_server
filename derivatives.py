from derivative_solver import Function
from derivative_solver import FUNCTION_TYPE
from derivative_solver import COEFF
from derivative_solver import DEGREE
from derivative_solver import INNER_FUNCTION
from derivative_solver import BASE
import math


# term is a 4-tuple  (COEFF, FUNCTION_TYPE, DEGREE/BASE, INNER_FUNCTION)

def poly(term):
    if not term[DEGREE]:
        return 0, Function.POLY, 0, None
    else:
        return term[COEFF] * term[DEGREE], Function.POLY, term[DEGREE] - 1, term[INNER_FUNCTION]


def sin(term):
    return term[COEFF], Function.COS, term[DEGREE], term[INNER_FUNCTION]


def cos(term):
    return -term[COEFF], Function.SIN, term[DEGREE], term[INNER_FUNCTION]


def tan(term):  # derivative of tan(x) is  1/(cos(x))^2
    return 1, Function.DIV, 1, [1, (1, Function.POLY, 2, (1, Function.COS, 1, term[INNER_FUNCTION]))]


def exp(term):
    return term[COEFF] * math.log(term[BASE]), Function.EXP, term[BASE], term[INNER_FUNCTION]


def log(term):
    return 1, Function.DIV, 1, [(term[COEFF] / math.log(term[BASE]), Function.POLY, 0, None), term[INNER_FUNCTION]]


def sqrt(term):
    return 1, Function.DIV, 1, [(term[COEFF], Function.POLY, 0, None), (2, Function.SQRT, 1, term[INNER_FUNCTION])]

derivatives = {
    Function.POLY: poly,
    Function.SQRT: sqrt,
    Function.EXP: exp,
    Function.LOG: log,
    Function.SIN: sin,
    Function.COS: cos,
    Function.TAN: tan
}








