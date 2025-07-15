from sympy import sympify, Eq
from solver.derivative_solver import DerivativeSolver
from solver.integration_solver import IntegrationSolver

def dispatch_problem(problem_str):
    """
    Detects problem type and calls appropriate solver.
    Returns (result, steps)
    """
    problem_str = problem_str.strip()

    if problem_str.lower().startswith("integrate_definite"):
        expr_str = problem_str[len("integrate_definite"):].strip()

        if ";" not in expr_str:
            return (
                "Error: Expected expression and bounds separated by ';'",
                ["Example: integrate_definite x**2 ; 0 ; 1"]
            )

        parts = [p.strip() for p in expr_str.split(";")]
        if len(parts) != 3:
            return (
                "Error: Must provide expression and two bounds.",
                ["Format: integrate_definite expression ; lower ; upper"]
            )

        expr = sympify(parts[0])
        lower = sympify(parts[1])
        upper = sympify(parts[2])

        solver = IntegrationSolver()
        result = solver.solve_definite(expr, lower, upper)
        steps = solver.explain_steps(expr)

        return result, steps


    elif problem_str.lower().startswith("diff_parametric"):
        expr_str = problem_str[len("diff_parametric"):].strip()
        # Expect format: y_expr ; x_expr
        if ";" not in expr_str:
            return (
                "Error: Expected two expressions separated by ';'",
                ["Format example: diff_parametric t**3 ; t**2"]
            )
        y_str, x_str = expr_str.split(";")
        y = sympify(y_str.strip())
        x = sympify(x_str.strip())

        solver = DerivativeSolver()
        result = solver.solve_parametric(x, y)
        steps = solver.explain_steps((x, y))
        return result, steps


    elif problem_str.lower().startswith("diff_implicit"):
        expr_str = problem_str[len("diff_implicit"):].strip()
        # Split into LHS=RHS
        if "=" not in expr_str:
            return "Error: Expected an equation with '='.", ["Format example: diff_implicit x**2 + y**2 = 1"]
        lhs_str, rhs_str = expr_str.split("=")
        lhs = sympify(lhs_str)
        rhs = sympify(rhs_str)
        solver = DerivativeSolver()
        result = solver.solve_implicit(Eq(lhs, rhs))
        steps = solver.explain_steps(Eq(lhs, rhs))
        return result, steps

    elif problem_str.lower().startswith("diff"):
        expr_str = problem_str[len("diff"):].strip()
        expr = sympify(expr_str)
        solver = DerivativeSolver()
        result = solver.solve(expr)
        steps = solver.explain_steps(expr)
        return result, steps

    elif problem_str.lower().startswith("integrate"):
        expr_str = problem_str[len("integrate"):].strip()
        expr = sympify(expr_str)
        solver = IntegrationSolver()
        result = solver.solve(expr)
        steps = solver.explain_steps(expr)
        return result, steps

    else:
        return "Unsupported problem type.", ["Please start input with 'diff', 'diff_implicit', or 'integrate'."]
