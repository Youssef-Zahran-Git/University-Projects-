import math
import re

print("Enter the equation in terms of x (e.g., e^-x - x, x^2 - 4, or 2x):")
eq_str = input("Equation: ")

eq_str = eq_str.lower()
eq_str = eq_str.replace('^', '**')
eq_str = re.sub(r'(\d)([a-z(])', r'\1*\2', eq_str)

math_env = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}


def f(x_val):
    env = math_env.copy()
    env['x'] = x_val
    return eval(eq_str, env)


iterations = int(input("Enter the number of iterations (e.g., 3): "))
is_modified = input("Do you want to use the Modified Secant Method? (yes/no): ").strip().lower()

if is_modified == 'yes' or is_modified == 'y':
    print("\n--- Modified Secant Method ---")
    x_curr = float(input("Enter the initial value x_0 (e.g., 1.0): "))
    delta = float(input("Enter the delta value (e.g., 0.01): "))

    for i in range(1, iterations + 1):
        f_curr = f(x_curr)
        f_delta = f(x_curr + (delta * x_curr))

        denominator = f_delta - f_curr

        if denominator == 0:
            print("Division by zero occurred. Calculation stopped.")
            break

        x_next = x_curr - (delta * x_curr * f_curr) / denominator
        print(f"Iteration {i}: x = {x_next:.6f}")

        x_curr = x_next

else:
    print("\n--- Standard Secant Method ---")
    x_prev = float(input("Enter the first initial value x_{-1} (e.g., 0): "))
    x_curr = float(input("Enter the second initial value x_0 (e.g., 1.0): "))

    for i in range(1, iterations + 1):
        f_prev = f(x_prev)
        f_curr = f(x_curr)

        denominator = f_prev - f_curr

        if denominator == 0:
            print("Division by zero occurred. Calculation stopped.")
            break

        x_next = x_curr - (f_curr * (x_prev - x_curr)) / denominator
        print(f"Iteration {i}: x = {x_next:.6f}")

        x_prev = x_curr
        x_curr = x_next