KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
INT_CONST = "INTEGER CONSTANT"
FLOAT_CONST = "FLOAT CONSTANT"
STRING_CONST = "STRING CONSTANT"
IDENTIFIER = "IDENTIFIER"
CLASS = "class"
METHOD = "method"
FUNCTION = "function"
CONSTRUCTOR = "constructor"
INT = "int"
BOOLEAN = "boolean"
CHAR = "char"
VOID = "void"
VAR = "var"
STATIC = "satic"
FIELD = "field"
LET = "let"
DO = "do"
IF = "if"
ELSE = "else"
WHILE = "while"
RETURN = "return"
TRUE = "true"
FALSE = "false"
NULL = "null"
THIS = "this"

TERMINALS = ["keyword", "symbol", "integerConstant", "stringConstant"]
KEYWORDS = ["class", "function", "method", "constructor", "var", "static",
            "field", "let", "do", "if", "else", "while", "return", "true",
            "false", "null", "this", "int", "char", "void", "boolean"]
STATEMENTS_KEYWORDS = ["let", "do", "if", "else", "while", "return"]
SUBROUTINE_KEYWORD = ["function", "method", "constructor"]
TYPE_KEYWORD = ["boolean", "int", "char", "void"]
CLASS_VAR_TYPE = ["static", "field"]

SYMBOLS = ["{", "}", "(", ")", "[", "]", ",", ";", "+", "-", "*", "^",
           "/", "&", "|", "<", ">", "=", "~", "!"]

SUPERSCRIPT_SYMBOLS = {
    1: "\u00B9",
    2: "\u00B2",
    3: "\u00B3",
    4: "\u2074",
    5: "\u2075",
    6: "\u2076",
    7: "\u2077",
    8: "\u2078",
    9: "\u2079",
    0: "\u2070",
}

SUBSCRIPT_SYMBOLS = {
    0: "\u2080",
    1: "\u2081",
    2: "\u2082",
    3: "\u2083",
    4: "\u2084",
    5: "\u2085",
    6: "\u2086",
    7: "\u2087",
    8: "\u2088",
    9: "\u2089"
}

OP = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "=", "^"]
UNARY_OP = ["~", "sin", "cos", "tan", "log", "exp", "!", "sqrt"]  # ~ is for negation

EXRESSION_TERMINATION = [";", ")", "]", ","]  # an expression ends in those symbols
INVALID_TOKEN = "COMPILATION ERROR : Invalid Token"

