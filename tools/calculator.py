def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


def calculate(a: float, operator: str, b: float):
    """Perform a mathematical calculation using two numbers and an operator."""

    print(f"\n[TOOL CALLED] calculate(a={a}, operator='{operator}', b={b})")

    if operator == "+":
        return add(a, b)

    if operator == "-":
        return subtract(a, b)

    if operator == "*":
        return multiply(a, b)

    if operator == "/":
        return divide(a, b)

    raise ValueError(f"Unsupported operator: {operator}")