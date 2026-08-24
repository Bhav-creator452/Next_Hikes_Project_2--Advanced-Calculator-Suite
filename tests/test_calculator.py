import pytest

from src.calculator import Calculator


def test_addition():
    assert Calculator.add(10, 5) == 15


def test_subtraction():
    assert Calculator.subtract(10, 5) == 5


def test_multiplication():
    assert Calculator.multiply(10, 5) == 50


def test_division():
    assert Calculator.divide(10, 5) == 2


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(10, 0)


def test_calculate_addition():
    assert Calculator.calculate(10, "+", 5) == 15


def test_calculate_subtraction():
    assert Calculator.calculate(10, "-", 5) == 5


def test_calculate_multiplication():
    assert Calculator.calculate(10, "×", 5) == 50


def test_calculate_division():
    assert Calculator.calculate(10, "÷", 5) == 2

def test_expression_with_operator_precedence():
    assert Calculator.evaluate_expression("25 + 10 × 2") == 45

def test_expression_with_parentheses():
    assert Calculator.evaluate_expression("(25 + 10) × 2") == 70


def test_parentheses_override_precedence():
    assert Calculator.evaluate_expression("25 + (10 × 2)") == 45