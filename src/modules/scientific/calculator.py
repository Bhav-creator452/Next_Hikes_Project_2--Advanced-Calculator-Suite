"""
Scientific calculator expression engine.

Deliberately does NOT use Python's eval(). Instead this is a small
hand-written tokenizer + recursive-descent parser + evaluator that only
understands numbers, + - * / ^ ! % (), and a fixed whitelist of
functions/constants. This keeps calculator input (untrusted user data)
from ever reaching arbitrary code execution.

Public entry point: evaluate(expression, angle_mode) -> float
Raises ScientificMathError with a user-friendly message on bad input.
"""
import math
import re
from typing import List, Union


class ScientificMathError(Exception):
    """Raised for any evaluable-but-invalid math, e.g. sqrt(-1), log(0)."""


class ExpressionError(Exception):
    """Raised for malformed expressions (bad syntax, unmatched parens, etc.)."""


CONSTANTS = {
    "pi": math.pi,
    "\u03c0": math.pi,
    "e": math.e,
}

# function name -> (arity, implementation taking already-evaluated args + angle_mode)
FUNCTIONS = {
    "sin", "cos", "tan", "asin", "acos", "atan",
    "log", "ln", "sqrt", "abs", "exp",
}

TOKEN_RE = re.compile(r"""
    \s*(?:
        (?P<number>\d+\.\d+|\.\d+|\d+)
      | (?P<ident>[A-Za-z_][A-Za-z_0-9]*)
      | (?P<op>\*\*|[+\-*/^!%(),])
    )
""", re.VERBOSE)


def tokenize(expr: str) -> List[str]:
    tokens = []
    pos = 0
    expr = expr.replace("\u00d7", "*").replace("\u00f7", "/").replace("\u2212", "-")
    while pos < len(expr):
        if expr[pos].isspace():
            pos += 1
            continue
        m = TOKEN_RE.match(expr, pos)
        if not m or m.end() == pos:
            raise ExpressionError("Invalid Expression")
        pos = m.end()
        tok = m.group("number") or m.group("ident") or m.group("op")
        tokens.append(tok)
    return tokens


class _Parser:
    """
    Recursive-descent parser/evaluator over a whitelist grammar:

        expr    := term (('+'|'-') term)*
        term    := unary (('*'|'/') unary)*
        unary   := ('-'|'+')? power
        power   := postfix ('^' unary)?
        postfix := atom ('!' | '%')*
        atom    := NUMBER | CONST | FUNC '(' expr ')' | '(' expr ')'
    """

    def __init__(self, tokens: List[str], angle_mode: str):
        self.tokens = tokens
        self.pos = 0
        self.angle_mode = angle_mode

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def expect(self, tok):
        if self.peek() != tok:
            raise ExpressionError("Invalid Expression")
        self.advance()

    def parse(self) -> float:
        if not self.tokens:
            raise ExpressionError("Invalid Expression")
        value = self.parse_expr()
        if self.pos != len(self.tokens):
            raise ExpressionError("Invalid Expression")
        return value

    def parse_expr(self) -> float:
        value = self.parse_term()
        while self.peek() in ("+", "-"):
            op = self.advance()
            rhs = self.parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def parse_term(self) -> float:
        value = self.parse_unary()
        while self.peek() in ("*", "/"):
            op = self.advance()
            rhs = self.parse_unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ScientificMathError("Division by Zero")
                value = value / rhs
        return value

    def parse_unary(self) -> float:
        if self.peek() == "-":
            self.advance()
            return -self.parse_unary()
        if self.peek() == "+":
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    def parse_power(self) -> float:
        base = self.parse_postfix()
        if self.peek() in ("^", "**"):
            self.advance()
            exponent = self.parse_unary()
            try:
                result = math.pow(base, exponent)
            except (ValueError, OverflowError):
                raise ScientificMathError("Math Error")
            if isinstance(result, complex):
                raise ScientificMathError("Math Error")
            return result
        return base

    def parse_postfix(self) -> float:
        value = self.parse_atom()
        while self.peek() in ("!", "%"):
            op = self.advance()
            if op == "!":
                value = _factorial(value)
            else:
                value = value / 100
        return value

    def parse_atom(self) -> float:
        tok = self.peek()
        if tok is None:
            raise ExpressionError("Invalid Expression")

        if tok == "(":
            self.advance()
            value = self.parse_expr()
            self.expect(")")
            return value

        if re.fullmatch(r"\d+\.\d+|\.\d+|\d+", tok):
            self.advance()
            return float(tok)

        if tok in CONSTANTS:
            self.advance()
            return CONSTANTS[tok]

        if tok in FUNCTIONS:
            self.advance()
            self.expect("(")
            arg = self.parse_expr()
            self.expect(")")
            return _apply_function(tok, arg, self.angle_mode)

        raise ExpressionError("Invalid Expression")


def _to_radians(value: float, angle_mode: str) -> float:
    if angle_mode == "DEG":
        return math.radians(value)
    if angle_mode == "GRAD":
        return value * (math.pi / 200)
    return value  # RAD


def _from_radians(value: float, angle_mode: str) -> float:
    if angle_mode == "DEG":
        return math.degrees(value)
    if angle_mode == "GRAD":
        return value * (200 / math.pi)
    return value


def _apply_function(name: str, arg: float, angle_mode: str) -> float:
    try:
        if name == "sin":
            return round(math.sin(_to_radians(arg, angle_mode)), 12)
        if name == "cos":
            return round(math.cos(_to_radians(arg, angle_mode)), 12)
        if name == "tan":
            rad = _to_radians(arg, angle_mode)
            cos_v = math.cos(rad)
            if abs(cos_v) < 1e-12:
                raise ScientificMathError("Undefined")
            return round(math.tan(rad), 12)
        if name == "asin":
            if not -1 <= arg <= 1:
                raise ScientificMathError("Math Error")
            return _from_radians(math.asin(arg), angle_mode)
        if name == "acos":
            if not -1 <= arg <= 1:
                raise ScientificMathError("Math Error")
            return _from_radians(math.acos(arg), angle_mode)
        if name == "atan":
            return _from_radians(math.atan(arg), angle_mode)
        if name == "log":
            if arg <= 0:
                raise ScientificMathError("Math Error")
            return math.log10(arg)
        if name == "ln":
            if arg <= 0:
                raise ScientificMathError("Math Error")
            return math.log(arg)
        if name == "sqrt":
            if arg < 0:
                raise ScientificMathError("Math Error")
            return math.sqrt(arg)
        if name == "abs":
            return abs(arg)
        if name == "exp":
            return math.exp(arg)
    except (ValueError, OverflowError):
        raise ScientificMathError("Math Error")
    raise ExpressionError("Invalid Expression")


def _factorial(value: float) -> float:
    if value < 0 or value != int(value):
        raise ScientificMathError("Math Error")
    if value > 170:
        raise ScientificMathError("Math Error")
    return float(math.factorial(int(value)))


def evaluate(expression: str, angle_mode: str = "DEG") -> float:
    """Tokenize, parse and evaluate a scientific expression safely."""
    if expression is None or expression.strip() == "":
        raise ExpressionError("Invalid Expression")
    tokens = tokenize(expression)
    # Balance parentheses defensively (UI should already keep them balanced).
    open_count = tokens.count("(")
    close_count = tokens.count(")")
    if close_count > open_count:
        raise ExpressionError("Invalid Expression")
    tokens += [")"] * (open_count - close_count)
    parser = _Parser(tokens, angle_mode)
    result = parser.parse()
    if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
        raise ScientificMathError("Undefined")
    return result
