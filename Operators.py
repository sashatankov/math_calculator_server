# UTILITY MODULE
import math


def neg(a):
    return -a


def add(a, b):
    return a + b


def diff(a, b):
    return a - b


def mult(a, b):
    return a * b


def div(a, b):
    return a / b


def power(a, b):
    return a ** b

operators = {"~": neg,
             "+": add,
             "-": diff,
             "*": mult,
             "/": div,
             "^": power,
             "!": math.factorial,
             "sqrt": math.sqrt,
             "\u221A": math.sqrt,
             "sin": math.sin,
             "cos": math.cos,
             "tan": math.tan,
             "log": math.log10,
             "exp": math.exp,
             "pi": math.pi,
             "e": math.e}
