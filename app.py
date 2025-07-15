import streamlit as st
from sympy import latex, symbols
from solver.dispatcher import dispatch_problem

# Optional plotting dependencies
from sympy import lambdify
import numpy as np
import matplotlib.pyplot as plt

# Streamlit page settings
st.set_page_config(page_title="Advanced Math Solver", page_icon="🧮")

# Title and instructions
st.markdown("### 🎯 How to Use This Solver")

st.markdown("**1.** `integrate x**2` — Indefinite integral of a function")
st.latex(r"\int x^2 \, dx = \frac{x^3}{3} + C")

st.markdown("**2.** `integrate_definite x**2 ; 0 ; 3` — Definite integral from 0 to 3")
st.latex(r"\int_0^3 x^2 \, dx = \left[ \frac{x^3}{3} \right]_0^3 = 9")

st.markdown("**3.** `diff x**3` — Derivative of a function")
st.latex(r"\frac{d}{dx} x^3 = 3x^2")

st.markdown("**4.** `diff_implicit x**2 + y**2 - 1` — Implicit differentiation of:")
st.latex(r"x^2 + y^2 = 1")
st.latex(r"\frac{dy}{dx}")

st.markdown("**5.** `diff_parametric t**3 ; t**2` — Parametric differentiation")
st.latex(r"x = t^3, \quad y = t^2")
st.latex(r"\frac{dy}{dx} = \frac{\frac{dy}{dt}}{\frac{dx}{dt}}")





# Input
command = st.text_input("Your command:")

# Solve button
if st.button("Solve"):
    if not command.strip():
        st.warning("Please enter a command.")
    else:
        result, steps = dispatch_problem(command)

        # Display result
        st.success("✅ Result:")
        try:
            result_latex = latex(result)
            st.latex(f"{result_latex}")
        except Exception:
            st.write(result)

        # Optional numeric evaluation
        if st.checkbox("🔢 Show numeric approximation"):
            try:
                approx = result.evalf()
                st.info(f"≈ {approx}")
            except:
                st.warning("Cannot evaluate numerically.")

        # Steps
        st.write("**📝 Steps:**")
        for step in steps:
            if "∫" in step or "^" in step or "=" in step:
                try:
                    st.latex(step)
                except Exception:
                    st.markdown(f"- {step}")
            else:
                st.markdown(f"- {step}")

        # Optional graph plotting
        if st.checkbox("📈 Plot result (function view)"):
            try:
                x = symbols('x')
                f = lambdify(x, result, modules=["numpy"])
                x_vals = np.linspace(-10, 10, 400)
                y_vals = f(x_vals)

                fig, ax = plt.subplots()
                ax.plot(x_vals, y_vals)
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_title("Graph of Result")
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"Unable to plot: {e}")

