from sage.all import *


def solve_equation(equation):
    """
    Solve an equation using the SageMath library.

    :param equation: str, the equation to solve.
    :return: str, the solution(s) as a formatted string.
    """
    try:
        # Parse the equation string into a SageMath expression
        eq = SvR(equation)
        # Solve the equation
        solutions = solve(eq, x)
        if solutions:
            # Format the solutions as strings
            solution_str = "\n".join(str(sol) for sol in solutions)
            return solution_str
        else:
            return "No real solutions found."
    except Exception as e:
        return f"Error: {e}"


# Example usage
equation = 'x^2 + 2*x + 1 == 0'
solution = solve_equation(equation)
print(f"Solved equation '{equation}':\n{solution}")
