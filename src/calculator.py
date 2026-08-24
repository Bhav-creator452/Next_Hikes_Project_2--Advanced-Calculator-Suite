class Calculator:
    """Core calculation engine for CalcSuite."""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    @staticmethod
    def calculate(a, operator, b):
        """Perform a calculation using the supplied operator."""

        if operator == "+":
            return Calculator.add(a, b)

        elif operator == "-":
            return Calculator.subtract(a, b)

        elif operator == "×":
            return Calculator.multiply(a, b)

        elif operator == "÷":
            return Calculator.divide(a, b)

        raise ValueError(f"Unsupported operator: {operator}")