from CompilationEngine import *
from equation_solver import *
from derivative_solver import *

def main():
    derivative_solver()


def expression_solver():
    data = "2^(4+2)"
    engine = CompilationEngine(data)
    res = engine.run()
    print(res)


def equation_solver():
    data = '2*(4x-8)=0'
    engine = EquationSolver(data)
    res = engine.solve()
    print(format_result(res))


def simplifier():
    data = "(5x-8)*(4x-8) + 4*(5x-6) -7+x^4"  # TODO to finish the simplifier
    engine = EquationSolver(data)
    res = engine.simplify()
    print(res)


def derivative_solver():
    data = "sin(x)"
    solver = DerivativeSolver(data)
    res = solver.derivative()
    print(res)


if __name__ == '__main__':
    main()
