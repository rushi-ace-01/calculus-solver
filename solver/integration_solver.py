# solver/integration_solver.py

from sympy import integrate, diff, Add, Mul, Pow, symbols, Function, log, simplify

class IntegrationSolver:
    def __init__(self):
        self.var = symbols('x')
        self.steps = []

    def solve(self, expr):
        self.steps.clear()
        result = self._integrate(expr)
        return result

    def explain_steps(self, expr):
        return self.steps
    

    def _integrate(self, expr) :
        num, den = None, None

        if (
            isinstance(expr, Mul)
            or isinstance(expr, Pow)
            or isinstance(expr, Add)
        ):
            if expr.is_Mul:
            # Try splitting numerator and denominator
                for arg in expr.args:
                    if arg.is_Pow and arg.exp == -1:
                        den = arg.base
                        rest = Mul(*[a for a in expr.args if a != arg])
                        num = rest
                        break

            if expr.is_Pow and expr.exp == -1:
                den = expr.base
                num = 1

            if den is not None:
                deriv_den = diff(den, self.var)
                if simplify(num - deriv_den) == 0:
                    from sympy import log
                    self.steps.append("Detected substitution: numerator is derivative of denominator.")
                    return log(den)
        # Base case: constant
        if expr.is_Number:
            self.steps.append(f"∫ {expr} dx = {expr} * x")
            return expr * self.var

        # Base case: variable x^n
        if expr == self.var:
            self.steps.append("∫ x dx = x^2 / 2")
            return self.var**2 / 2

        # Sum Rule
        if isinstance(expr, Add):
            self.steps.append("Using Sum Rule:")
            parts = [self._integrate(arg) for arg in expr.args]
            return sum(parts)

        # Power Rule
        if isinstance(expr, Pow):
            base, exp = expr.args
            if base == self.var:
                n = exp
                if n != -1:
                    res = self.var**(n + 1) / (n + 1)
                    self.steps.append(f"Using Power Rule: ∫ x^{n} dx = x^{n+1}/({n+1})")
                    return res
                else:
                    self.steps.append("Special case: ∫ 1/x dx = log(x)")
                    return log(self.var)

        # Product Rule for Integration by Parts
        if isinstance(expr, Mul):
            self.steps.append("Detected product: applying Integration by Parts.")
            
            # Auto-select u and dv
            def pick_u_and_dv(factors):
                """
                Applies LIATE heuristic to choose u and dv.
                Returns (u, dv).
                """
                priority = {
                    'log': 1,
                    'asin': 2, 'acos': 2, 'atan': 2,
                    'Symbol': 3, 'Pow': 3,
                    'sin': 4, 'cos': 4, 'tan': 4,
                    'exp': 5
                }

                # Assign a priority to each factor
                scored = []
                for f in factors:
                    if f.func.__name__ in priority:
                        score = priority[f.func.__name__]
                    elif f.is_Pow:
                        score = priority['Pow']
                    elif f.is_Symbol:
                        score = priority['Symbol']
                    else:
                        score = 99
                    scored.append((score, f))

                # The one with the lowest score becomes u
                scored.sort()
                u = scored[0][1]
                dv_factors = [f for s, f in scored[1:]]
                if not dv_factors:
                    dv = 1
                else:
                    from sympy import Mul
                    dv = Mul(*dv_factors)

                return u, dv

            u, dv = pick_u_and_dv(expr.args)

            
            self.steps.append(f"Let u = {u}")
            self.steps.append(f"Let dv = {dv} dx")
            
            # Compute du = d(u)
            du = diff(u, self.var)
            self.steps.append(f"Compute du = d(u)/dx dx = {du} dx")
            
            # Compute v = ∫ dv
            v = integrate(dv, self.var)
            self.steps.append(f"Compute v = ∫ dv = {v}")
            
            # Compute u*v
            uv = u * v
            
            self.steps.append(f"Compute u*v = {uv}")
            
            # Compute ∫ v du
            integral_vdu = integrate(v * du, self.var)
            self.steps.append(f"Compute ∫ v du = {integral_vdu}")
            
            # Final result
            result = uv - integral_vdu
            
            self.steps.append("Integration by Parts formula applied:")
            self.steps.append("∫ u dv = u*v - ∫ v du")
            
            return result

        # Fallback to SymPy
        self.steps.append("Used SymPy general integration.")
        return integrate(expr, self.var)
    
    def solve_definite(self, expr, lower, upper):
        """
        Computes definite integral ∫_{lower}^{upper} expr dx.
        """
        self.steps.clear()

        self.steps.append(f"Compute indefinite integral ∫ {expr} dx.")

        # Compute indefinite integral first
        F = self._integrate(expr)

        self.steps.append(f"Indefinite integral F(x) = {F}")

        # Evaluate at upper bound
        F_upper = F.subs(self.var, upper)
        self.steps.append(f"Evaluate F({upper}) = {F_upper}")

        # Evaluate at lower bound
        F_lower = F.subs(self.var, lower)
        self.steps.append(f"Evaluate F({lower}) = {F_lower}")

        # Compute difference
        result = simplify(F_upper - F_lower)

        self.steps.append(f"Definite integral = F({upper}) - F({lower}) = {result}")

        return result
        
            
            
            
