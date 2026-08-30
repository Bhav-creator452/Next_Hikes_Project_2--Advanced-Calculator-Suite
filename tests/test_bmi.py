import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from src.modules.bmi.calculator import calculate_bmi, categorize, to_kg, to_cm


def test_normal_bmi():
    result = calculate_bmi(weight_kg=70, height_cm=175)
    assert result.category == "Normal"
    assert 22 <= result.bmi <= 23


def test_underweight_boundary():
    assert categorize(18.4) == "Underweight"


def test_normal_boundary_low():
    assert categorize(18.5) == "Normal"


def test_normal_boundary_high():
    assert categorize(24.9) == "Normal"


def test_overweight_boundary():
    assert categorize(25.0) == "Overweight"


def test_obese_boundary():
    assert categorize(30.0) == "Obese"


def test_pound_to_kg_conversion():
    assert abs(to_kg(154.324, "lb") - 70) < 0.01


def test_ftin_to_cm_conversion():
    # 5 ft 9 in = 175.26 cm
    assert abs(to_cm(0, "ft-in", height_ft=5, height_in=9) - 175.26) < 0.1


def test_zero_weight_raises():
    with pytest.raises(ValueError):
        calculate_bmi(0, 170)


def test_negative_height_raises():
    with pytest.raises(ValueError):
        calculate_bmi(70, -170)
