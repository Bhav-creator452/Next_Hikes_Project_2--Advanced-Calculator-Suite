import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from src.modules.scientific.calculator import evaluate, ExpressionError, ScientificMathError


def test_sin_zero_degrees():
    assert abs(evaluate("sin(0)", "DEG")) < 1e-9


def test_cos_zero_degrees():
    assert abs(evaluate("cos(0)", "DEG") - 1) < 1e-9


def test_sin_90_degrees():
    assert abs(evaluate("sin(90)", "DEG") - 1) < 1e-9


def test_sqrt():
    assert evaluate("sqrt(16)") == 4


def test_log_base_10():
    assert abs(evaluate("log(100)") - 2) < 1e-9


def test_ln():
    import math
    assert abs(evaluate("ln(1)")) < 1e-9


def test_power():
    assert evaluate("2^3") == 8


def test_factorial():
    assert evaluate("5!") == 120


def test_factorial_zero():
    assert evaluate("0!") == 1


def test_parentheses_simple():
    assert evaluate("(5)") == 5


def test_parentheses_expression():
    assert evaluate("(5 + 3)") == 8


def test_nested_power_parens():
    assert evaluate("2^(3)") == 8


def test_sqrt_negative_raises_math_error():
    with pytest.raises(ScientificMathError):
        evaluate("sqrt(-1)")


def test_log_zero_raises_math_error():
    with pytest.raises(ScientificMathError):
        evaluate("log(0)")


def test_division_by_zero_raises():
    with pytest.raises(ScientificMathError):
        evaluate("10/0")


def test_tan_90_degrees_undefined():
    with pytest.raises(ScientificMathError):
        evaluate("tan(90)", "DEG")


def test_invalid_parentheses_raises_expression_error():
    with pytest.raises(ExpressionError):
        evaluate("5 + )")


def test_pi_constant():
    import math
    assert abs(evaluate("pi") - math.pi) < 1e-9


def test_reciprocal():
    assert evaluate("1/4") == 0.25


def test_degree_radian_switch():
    import math
    deg_result = evaluate("sin(30)", "DEG")
    rad_result = evaluate(f"sin({math.pi/6})", "RAD")
    assert abs(deg_result - rad_result) < 1e-6


def test_empty_expression_raises():
    with pytest.raises(ExpressionError):
        evaluate("")


def test_no_arbitrary_code_execution():
    # Anything not in the whitelist grammar must fail safely, never execute.
    with pytest.raises((ExpressionError, ScientificMathError)):
        evaluate("__import__('os')")
