from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from CompilationEngine import *
from equation_solver import *
from derivative_solver import *
from flask_cors import CORS, cross_origin


app = Flask(__name__, static_folder="build/static", template_folder="build")
CORS(app)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST", "OPTIONS"])
@cross_origin(origin="*")
def evaluate():
    data = request.json["expression"]
    print(data)
    res = str()
    try:
        engine = CompilationEngine(data)
        res = engine.run()
        print("res " + str(res))
    except CompilationError:
        res = "Invalid Expression"
    finally:
        return jsonify(result=res)


@app.route("/solve", methods=['POST', "OPTIONS"])
@cross_origin(origin="*")
def solve():
    data = request.json["expression"]
    print(data)
    res = str()
    try:
        solver = EquationSolver(data)
        roots = solver.solve()
        formatted_roots = format_result(roots)
        res = formatted_roots
        print(res)
    except CompilationError:
        res = "Invalid Expression"
    finally:
        return jsonify(result=res)


@app.route("/simplify", methods=["POST", "METHODS"])
@cross_origin("*")
def simplify():
    data = request.json["expression"]
    print(data)
    res = str()
    try:
        solver = EquationSolver(data    )
        simplified = solver.simplify()
        res = simplified
        print(res)
    except CompilationError:
        res = "Invalid Expression"
    finally:
        return jsonify(result=res)


@app.route("/derivative", methods=["POST", "METHODS"])
@cross_origin("*")
def derivative():
    data = request.json["expression"]
    print(data)
    res = str()
    try:
        solver = DerivativeSolver(data)
        der = solver.derivative()
        res = der
        print(res)
    except CompilationError:
        res = "Invalid Expression"
    finally:
        return jsonify(result=res)

if __name__ == '__main__':
    app.run(debug=True)
