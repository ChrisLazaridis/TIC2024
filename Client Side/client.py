from sage.all import *

# Example: Solve a simple equation
x = var('x')
equation = x**2 - 4 == 0
solutions = solve(equation, x)
print(solutions)