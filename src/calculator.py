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

    @staticmethod
    def evaluate_expression(expression):
        """
    Evaluate a complete arithmetic expression.

    Supports:
    - Addition (+)
    - Subtraction (-)
    - Multiplication (× or *)
    - Division (÷ or /)
    - Parentheses
    - Decimal numbers
        """
        if not isinstance(expression, str):
            raise TypeError("Expression must be a string")

        expression = expression.strip()

        if not expression:
            raise ValueError("Expression cannot be empty")

        parser = _ExpressionParser(expression)

        return parser.parse()

class _ExpressionParser:
    """Parser for arithmetic expressions."""

    def __init__(self, expression):
        self.expression = expression
        self.position = 0

    def parse(self):
        result = self._parse_expression()

        self._skip_spaces()

        if self.position != len(self.expression):
            raise ValueError(
                f"Unexpected character: {self.expression[self.position]}"
            )

        return result

    def _parse_expression(self):
        """Handle addition and subtraction."""
        result = self._parse_term()

        while True:
            operator = self._match("+", "-")

            if operator is None:
                break

            right = self._parse_term()

            if operator == "+":
                result += right
            else:
                result -= right

        return result

    def _parse_term(self):
        """Handle multiplication and division."""
        result = self._parse_factor()

        while True:
            operator = self._match("×", "*", "÷", "/")

            if operator is None:
                break

            right = self._parse_factor()

            if operator in ("×", "*"):
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Cannot divide by zero")

                result /= right

        return result

    def _parse_factor(self):
        """Handle numbers, parentheses, and unary signs."""
        sign = 1

        while True:
            operator = self._match("+", "-")

            if operator is None:
                break

            if operator == "-":
                sign *= -1

        self._skip_spaces()

        if self._match("("):
            result = self._parse_expression()

            if self._match(")") is None:
                raise ValueError("Missing closing parenthesis")
        else:
            result = self._parse_number()

        return sign * result

    def _parse_number(self):
        """Parse a decimal number from the expression."""
        self._skip_spaces()

        start = self.position
        decimal_seen = False
        digit_seen = False

        while self.position < len(self.expression):
            character = self.expression[self.position]

            if character.isdigit():
                digit_seen = True
                self.position += 1

            elif character == "." and not decimal_seen:
                decimal_seen = True
                self.position += 1

            else:
                break

        if not digit_seen:
            raise ValueError(
                f"Expected a number at position {self.position}"
        )

        number_text = self.expression[start:self.position]

        return float(number_text)

    def _skip_spaces(self):
        while (
            self.position < len(self.expression)
            and self.expression[self.position].isspace()
    ):
            self.position += 1

    def _match(self, *characters):
        self._skip_spaces()

        if (
            self.position < len(self.expression)
            and self.expression[self.position] in characters
        ):
            character = self.expression[self.position]
            self.position += 1
            return character

        return None