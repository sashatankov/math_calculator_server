from derivative_solver import Function
from derivative_solver import FUNCTION_TYPE
from derivative_solver import COEFF
from derivative_solver import DEGREE
from derivative_solver import INNER_FUNCTION
from derivative_solver import BASE


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


def tan(term):
    pass


def exp(term):
    pass


def log(term):
    pass


def sqrt(term):
    pass










