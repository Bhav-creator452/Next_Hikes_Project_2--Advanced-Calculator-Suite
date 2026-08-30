import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modules.standard.calculator import StandardCalculator, CalculatorState


def run(ops):
    """Helper: feed a sequence of ('type', value) instructions into a fresh calculator."""
    calc = StandardCalculator()
    for kind, val in ops:
        getattr(calc, kind)(val) if val is not None else getattr(calc, kind)()
    return calc


def test_basic_addition():
    calc = StandardCalculator()
    calc.input_digit("2")
    calc.input_operator("+")
    calc.input_digit("2")
    assert calc.equals() == 4


def test_basic_subtraction():
    calc = StandardCalculator()
    for d in "10":
        calc.input_digit(d)
    calc.input_operator("-")
    calc.input_digit("5")
    assert calc.equals() == 5


def test_multiplication():
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.input_operator("\u00d7")
    calc.input_digit("4")
    assert calc.equals() == 20


def test_division():
    calc = StandardCalculator()
    for d in "20":
        calc.input_digit(d)
    calc.input_operator("\u00f7")
    calc.input_digit("4")
    assert calc.equals() == 5


def test_division_by_zero():
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.input_operator("\u00f7")
    calc.input_digit("0")
    assert calc.equals() is None
    assert calc.state == CalculatorState.ERROR
    assert calc.error == "Division by Zero"


def test_decimal_addition():
    calc = StandardCalculator()
    calc.input_digit("0")
    calc.input_decimal()
    calc.input_digit("1")
    calc.input_operator("+")
    calc.input_digit("0")
    calc.input_decimal()
    calc.input_digit("2")
    result = calc.equals()
    assert abs(result - 0.3) < 1e-9


def test_negative_number_addition():
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.toggle_sign()
    calc.input_operator("+")
    calc.input_digit("1")
    calc.input_digit("0")
    assert calc.equals() == 5


def test_chained_calculation_precedence():
    # 2 + 3 * 4 should respect standard operator precedence
    calc = StandardCalculator()
    calc.input_digit("2")
    calc.input_operator("+")
    calc.input_digit("3")
    calc.input_operator("\u00d7")
    calc.input_digit("4")
    assert calc.equals() == 14


def test_operator_replacement():
    # 5 + x  -> operator should replace, not create "5 + x" invalid state
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.input_operator("+")
    calc.input_operator("\u00d7")
    calc.input_digit("2")
    assert calc.equals() == 10


def test_post_equals_continue_with_operator():
    calc = StandardCalculator()
    calc.input_digit("2")
    calc.input_digit("5")
    calc.equals()
    assert calc.tokens == ["25"]
    calc.input_operator("+")
    calc.input_digit("1")
    calc.input_digit("0")
    assert calc.equals() == 35


def test_post_equals_new_number_starts_fresh():
    calc = StandardCalculator()
    calc.input_digit("2")
    calc.input_digit("5")
    calc.equals()
    calc.input_digit("7")
    assert calc.tokens == ["7"]  # not "257"


def test_backspace_removes_last_digit():
    calc = StandardCalculator()
    for d in "12345":
        calc.input_digit(d)
    calc.backspace()
    assert calc.tokens[-1] == "1234"


def test_backspace_on_empty_is_safe():
    calc = StandardCalculator()
    calc.backspace()
    assert calc.tokens == ["0"]


def test_prevent_multiple_decimal_points():
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.input_decimal()
    calc.input_digit("2")
    calc.input_decimal()  # should be ignored
    calc.input_digit("3")
    assert calc.tokens[-1] == "5.23"


def test_negative_times_negative():
    calc = StandardCalculator()
    calc.input_open_paren()
    calc.input_digit("5")
    calc.toggle_sign()
    calc.input_close_paren()
    calc.input_operator("\u00d7")
    calc.input_open_paren()
    calc.input_digit("2")
    calc.toggle_sign()
    calc.input_close_paren()
    assert calc.equals() == 10


def test_percentage():
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.input_digit("0")
    calc.input_percent()
    assert calc.tokens[-1] == "0.5"


def test_clear_resets_state():
    calc = StandardCalculator()
    calc.input_digit("9")
    calc.clear()
    assert calc.tokens == ["0"]
    assert calc.state == CalculatorState.INITIAL


def test_double_equals_is_stable():
    calc = StandardCalculator()
    calc.input_digit("5")
    calc.input_operator("+")
    calc.input_digit("3")
    assert calc.equals() == 8
    # Pressing = again with no new operator shouldn't crash or corrupt state.
    result2 = calc.equals()
    assert result2 == 8
