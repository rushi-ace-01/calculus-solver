# solver/derivative_solver.py
from sympy.core.symbol import Symbol
from sympy import log
from sympy import Dummy
from sympy import diff, Mul, Add, Pow, Function, symbols, solve, Eq

class DerivativeSolver:
    def __init__(self):
        # Define variables
        self.x, self.y = symbols('x y')
        self.var = self.x  # Default variable of differentiation
        self.steps = []

    def solve(self, expr):
        self.steps.clear()
        result = self._differentiate(expr)
        return result

    def explain_steps(self, expr):
        return self.steps

    def _differentiate(self, expr):
        # Base cases
        if expr.is_Number:
            self.steps.append(f"d/dx[{expr}] = 0 (constant rule)")
            return 0

        if expr == self.var:
            self.steps.append(f"d/dx[x] = 1 (identity rule)")
            return 1

        # Sum Rule
        if isinstance(expr, Add):
            self.steps.append("Using Sum Rule:")
            return Add(*[self._differentiate(arg) for arg in expr.args])

        # Product Rule
        if isinstance(expr, Mul):
            self.steps.append("Using Product Rule:")
            terms = expr.args
            result = 0
            for i in range(len(terms)):
                d_term = self._differentiate(terms[i])
                rest = Mul(*[terms[j] for j in range(len(terms)) if j != i])
                part = d_term * rest
                self.steps.append(f"  d/dx[{terms[i]}] * {rest} = {part}")
                result += part
            return result

        # Power Rule
        if isinstance(expr, Pow):
            base, exp = expr.args
            if isinstance(exp, (int, float)) or exp.is_Number:
                result = exp * base**(exp - 1) * self._differentiate(base)
                self.steps.append(f"Using Power Rule: d/dx[{expr}] = {result}")
                return result

        # Chain Rule for functions like sin(x²), log(x²)
        # Chain Rule for functions like sin(x**2), log(x**3+1), cos(sqrt(x))
        if isinstance(expr, Function):
            inner = expr.args[0]
            
            # Create a dummy symbol u
            u = symbols('u')
            
            # Rebuild the function as f(u)
            func_u = expr.func(u)
            
            # Differentiate outer function f(u) w.r.t. u
            outer_diff = diff(func_u, u)
            
            # Differentiate inner expression w.r.t. x
            inner_diff = self._differentiate(inner)
            
            # Substitute back u = inner
            outer_diff_substituted = outer_diff.subs(u, inner)
            
            result = outer_diff_substituted * inner_diff
            
            self.steps.append(
                f"Using Chain Rule: d/dx[{expr}] = d/d({inner})[{expr}] * d/dx[{inner}] = {outer_diff_substituted} * {inner_diff} = {result}"
            )
            return result


        # Fallback
        result = diff(expr, self.var)
        self.steps.append(f"Fallback: d/dx[{expr}] = {result}")
        return result

    def solve_implicit(self, eq):
        """
        eq: Eq(lhs, rhs)
        """
        self.steps.clear()

        dy_dx = symbols('dy_dx')

        self.steps.append("Differentiate both sides with respect to x, treating y as a function of x.")

        lhs_diff = diff(eq.lhs, self.x) + diff(eq.lhs, self.y)*dy_dx
        rhs_diff = diff(eq.rhs, self.x) + diff(eq.rhs, self.y)*dy_dx

        self.steps.append(f"d/dx[LHS]: {lhs_diff}")
        self.steps.append(f"d/dx[RHS]: {rhs_diff}")

        new_eq = Eq(lhs_diff, rhs_diff)
        self.steps.append(f"Form the equation: {new_eq}")

        solution = solve(new_eq, dy_dx)

        if solution:
            self.steps.append(f"Solve for dy/dx: dy/dx = {solution[0]}")
            return solution[0]
        else:
            self.steps.append("Could not solve for dy/dx.")
            return None
        
    def solve_parametric(self, x_expr, y_expr, t_var=None):
        """
        x_expr: sympy expression for x(t)
        y_expr: sympy expression for y(t)
        t_var: sympy symbol for the parameter (default 't')
        """
        self.steps.clear()

        if t_var is None:
            t = symbols('t')
        else:
            t = t_var

        self.steps.append("Differentiate y(t) with respect to t.")
        dy_dt = diff(y_expr, t)
        self.steps.append(f"dy/dt = {dy_dt}")

        self.steps.append("Differentiate x(t) with respect to t.")
        dx_dt = diff(x_expr, t)
        self.steps.append(f"dx/dt = {dx_dt}")

        if dx_dt == 0:
            self.steps.append("Error: dx/dt = 0, cannot divide.")
            return None

        dydx = dy_dt / dx_dt
        self.steps.append(f"dy/dx = (dy/dt) / (dx/dt) = {dydx}")
        return dydx