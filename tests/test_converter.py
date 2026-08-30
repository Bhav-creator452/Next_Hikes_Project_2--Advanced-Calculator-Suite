import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from src.modules.converter.converter import convert, get_categories, get_units


def test_meters_to_kilometers():
    assert convert("Length", 1000, "Meter", "Kilometer") == 1.0


def test_kg_to_grams():
    assert convert("Weight", 1, "Kilogram", "Gram") == 1000.0


def test_celsius_to_fahrenheit():
    assert abs(convert("Temperature", 0, "Celsius", "Fahrenheit") - 32) < 1e-9


def test_fahrenheit_to_celsius():
    assert abs(convert("Temperature", 212, "Fahrenheit", "Celsius") - 100) < 1e-9


def test_celsius_to_kelvin():
    assert abs(convert("Temperature", 0, "Celsius", "Kelvin") - 273.15) < 1e-9


def test_same_unit_returns_same_value():
    assert convert("Length", 42, "Meter", "Meter") == 42


def test_unknown_category_raises():
    with pytest.raises(ValueError):
        convert("NotACategory", 1, "A", "B")


def test_unknown_unit_raises():
    with pytest.raises(ValueError):
        convert("Length", 1, "Meter", "NotAUnit")


def test_categories_include_temperature():
    assert "Temperature" in get_categories()


def test_length_units_present():
    units = get_units("Length")
    assert "Meter" in units and "Mile" in units


def test_round_trip_conversion():
    value = 12.5
    km = convert("Length", value, "Mile", "Kilometer")
    back = convert("Length", km, "Kilometer", "Mile")
    assert abs(back - value) < 1e-6
