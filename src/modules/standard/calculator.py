"""
Standard calculator engine.

Pure logic, independently testable from the UI. Implements a small
explicit state machine (see CalculatorState) instead of scattered
boolean flags, per the project's architecture rules.

Supported operators: + - x / %
Supports chained calculations, operator replacement, post-equals
continuation, +/- toggle and safe backspace — all without fragile
string surgery on the whole expression.
"""
from enum import Enum, auto
from typing import List, Union, Optional

from src.utils.formatting import format_number

Token = Union[float, str]  # numbers as float, operators/parens as str
OPERATORS = ("+", "-", "\u00d7", "\u00f7")
OP_MAP = {"+": "+", "-": "-", "\u00d7": "*", "\u00f7": "/"}


class CalculatorState(Enum):
    INITIAL = auto()
    ENTERING_NUMBER = auto()
    ENTERING_DECIMAL = auto()
    ENTERING_OPERATOR = auto()
    SHOWING_RESULT = auto()
    AFTER_EQUALS = auto()
    ERROR = auto()


class StandardCalculator:
    """
    Token-based calculator. `tokens` holds numbers (as strings, to
    preserve exact user entry like "5." while typing) and operators.
    """

    def __init__(self):
        self.reset()

    # ---- state ----------------------------------------------------
    def reset(self) -> None:
        self.tokens: List[str] = ["0"]
        self.state: CalculatorState = CalculatorState.INITIAL
        self.last_result: Optional[float] = None
        self.error: Optional[str] = None

    def clear(self) -> None:
        self.reset()

    # ---- public API -------------------------------------------------
    def input_digit(self, digit: str) -> None:
        if self.state == CalculatorState.ERROR:
            self.reset()

        if self.state in (CalculatorState.SHOWING_RESULT, CalculatorState.AFTER_EQUALS):
            # A fresh number after "=" starts a brand-new calculation.
            self.tokens = ["0"]
            self.state = CalculatorState.INITIAL

        current = self.tokens[-1]
        if current in OPERATORS or current in ("(", ")"):
            self.tokens.append(digit if digit != "0" else "0")
        else:
            if current == "0":
                self.tokens[-1] = digit
            else:
                self.tokens[-1] = current + digit

        self.state = CalculatorState.ENTERING_NUMBER

    def input_decimal(self) -> None:
        if self.state == CalculatorState.ERROR:
            self.reset()
        if self.state in (CalculatorState.SHOWING_RESULT, CalculatorState.AFTER_EQUALS):
            self.tokens = ["0"]
            self.state = CalculatorState.INITIAL

        current = self.tokens[-1]
        if current in OPERATORS or current in ("(", ")"):
            self.tokens.append("0.")
        elif "." not in current:
            self.tokens[-1] = current + "."
        # else: already has a decimal point -> ignore (prevents "5.2.3")

        self.state = CalculatorState.ENTERING_DECIMAL

    def input_operator(self, op: str) -> None:
        if self.state == CalculatorState.ERROR:
            return
        if op not in OPERATORS:
            return

        if self.state == CalculatorState.SHOWING_RESULT and self.last_result is not None:
            # Continue from previous result: 25 = , + , 10 , = -> 35
            self.tokens = [self._fmt_operand(self.last_result)]

        current = self.tokens[-1]
        if current in OPERATORS:
            # Operator replacement: "5 + x" -> "5 x" (never an invalid trailing op run)
            self.tokens[-1] = op
        elif current == "(":
            # Can't place a binary operator right after "("; ignore except unary minus.
            if op == "-":
                self.tokens.append("-0")
        else:
            self.tokens.append(op)

        self.state = CalculatorState.ENTERING_OPERATOR

    def input_open_paren(self) -> None:
        if self.state == CalculatorState.ERROR:
            self.reset()
        current = self.tokens[-1]
        if current in OPERATORS or current == "(":
            self.tokens.append("(")
        elif current == "0" and len(self.tokens) == 1:
            self.tokens[-1] = "("
        else:
            # implicit multiplication: 5( -> 5 * (
            self.tokens.append("*")
            self.tokens.append("(")
        self.state = CalculatorState.ENTERING_OPERATOR

    def input_close_paren(self) -> None:
        if self.state == CalculatorState.ERROR:
            return
        open_count = self.tokens.count("(")
        close_count = self.tokens.count(")")
        if open_count > close_count and self.tokens[-1] not in OPERATORS and self.tokens[-1] != "(":
            self.tokens.append(")")
            self.state = CalculatorState.ENTERING_OPERATOR

    def toggle_sign(self) -> None:
        if self.state == CalculatorState.ERROR:
            return
        current = self.tokens[-1]
        if current in OPERATORS or current in ("(", ")"):
            return
        if current.startswith("-"):
            self.tokens[-1] = current[1:]
        else:
            self.tokens[-1] = "-" + current

    def input_percent(self) -> None:
        if self.state == CalculatorState.ERROR:
            return
        current = self.tokens[-1]
        if current in OPERATORS or current in ("(", ")"):
            return
        try:
            value = float(current) / 100
        except ValueError:
            return
        self.tokens[-1] = self._fmt_operand(value)

    def backspace(self) -> None:
        if self.state == CalculatorState.ERROR:
            self.reset()
            return
        if self.state in (CalculatorState.SHOWING_RESULT, CalculatorState.AFTER_EQUALS):
            self.reset()
            return

        current = self.tokens[-1]
        if current in OPERATORS or current in ("(", ")"):
            self.tokens.pop()
            if not self.tokens:
                self.tokens = ["0"]
        else:
            trimmed = current[:-1]
            if trimmed in ("", "-"):
                if len(self.tokens) > 1:
                    self.tokens.pop()
                else:
                    self.tokens[-1] = "0"
            else:
                self.tokens[-1] = trimmed
        if not self.tokens:
            self.tokens = ["0"]

    def equals(self) -> Optional[float]:
        if self.state == CalculatorState.ERROR:
            return None
        try:
            result = self._evaluate()
        except (ZeroDivisionError,):
            self.error = "Division by Zero"
            self.state = CalculatorState.ERROR
            return None
        except Exception:
            self.error = "Invalid Expression"
            self.state = CalculatorState.ERROR
            return None

        self.last_result = result
        self.tokens = [self._fmt_operand(result)]
        self.state = CalculatorState.SHOWING_RESULT
        self.error = None
        return result

    # ---- display helpers --------------------------------------------
    def get_expression_display(self) -> str:
        return " ".join(self.tokens)

    def get_result_preview(self) -> Optional[str]:
        """Live preview of the result while typing, or None if not evaluable."""
        if self.state == CalculatorState.ERROR:
            return self.error
        try:
            value = self._evaluate(strict=False)
            if value is None:
                return None
            return format_number(value)
        except Exception:
            return None

    # ---- internal -----------------------------------------------------
    def _fmt_operand(self, value: float) -> str:
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return repr(round(value, 12))

    def _evaluate(self, strict: bool = True) -> Optional[float]:
        expr_tokens = list(self.tokens)

        # Drop a trailing dangling operator for a *preview* (not for '=').
        while expr_tokens and expr_tokens[-1] in OPERATORS:
            if strict:
                break
            expr_tokens = expr_tokens[:-1]

        if not expr_tokens:
            return None

        # Auto-close unmatched parentheses.
        open_count = expr_tokens.count("(")
        close_count = expr_tokens.count(")")
        expr_tokens += [")"] * max(0, open_count - close_count)

        py_expr = self._to_python_expression(expr_tokens)
        if py_expr is None:
            if strict:
                raise ValueError("invalid expression")
            return None

        value = _safe_eval_arithmetic(py_expr)
        return value

    def _to_python_expression(self, tokens: List[str]) -> Optional[str]:
        parts = []
        for tok in tokens:
            if tok in OPERATORS:
                parts.append(OP_MAP[tok])
            elif tok in ("(", ")"):
                parts.append(tok)
            else:
                try:
                    float(tok)
                except ValueError:
                    return None
                parts.append(tok)
        return " ".join(parts)


def _safe_eval_arithmetic(expression: str) -> float:
    """
    Evaluate a plain +-*/() arithmetic expression using Python's ast
    module rather than eval(), so no arbitrary code can be executed.
    """
    import ast
    import operator

    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("invalid literal")
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError()
            return allowed_ops[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.operand))
        raise ValueError("disallowed expression")

    tree = ast.parse(expression, mode="eval")
    return _eval(tree)
