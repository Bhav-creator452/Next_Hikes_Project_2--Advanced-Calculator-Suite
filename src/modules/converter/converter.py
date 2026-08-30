"""
General-purpose unit converter engine.

Kept fully separate from the UI. Categories are defined as structured
data (`CATEGORIES`) rather than scattered if/else chains, so adding a
new category later just means adding a dict entry.

Most categories use a simple "multiply by factor relative to a base
unit" model. Temperature needs real formulas, so it's handled specially.
"""
from typing import Dict

# Each category maps unit_name -> multiplier relative to the category's base unit.
CATEGORIES: Dict[str, Dict[str, float]] = {
    "Length": {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.344,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
    },
    "Weight": {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.45359237,
        "Ounce": 0.028349523125,
    },
    "Area": {
        "Square Meter": 1.0,
        "Square Kilometer": 1_000_000.0,
        "Square Foot": 0.09290304,
        "Square Yard": 0.83612736,
        "Acre": 4046.8564224,
        "Hectare": 10_000.0,
    },
    "Volume": {
        "Liter": 1.0,
        "Milliliter": 0.001,
        "Cubic Meter": 1000.0,
        "Gallon (US)": 3.785411784,
        "Quart (US)": 0.946352946,
        "Cup (US)": 0.2365882365,
    },
    "Time": {
        "Second": 1.0,
        "Millisecond": 0.001,
        "Minute": 60.0,
        "Hour": 3600.0,
        "Day": 86400.0,
        "Week": 604800.0,
    },
    "Speed": {
        "Meter/second": 1.0,
        "Kilometer/hour": 0.277778,
        "Mile/hour": 0.44704,
        "Knot": 0.514444,
    },
    "Data": {
        "Byte": 1.0,
        "Kilobyte": 1024.0,
        "Megabyte": 1024.0 ** 2,
        "Gigabyte": 1024.0 ** 3,
        "Terabyte": 1024.0 ** 4,
        "Bit": 0.125,
    },
}

TEMPERATURE_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]


def get_categories():
    return list(CATEGORIES.keys()) + ["Temperature"]


def get_units(category: str):
    if category == "Temperature":
        return list(TEMPERATURE_UNITS)
    return list(CATEGORIES.get(category, {}).keys())


def convert(category: str, value: float, from_unit: str, to_unit: str) -> float:
    if category == "Temperature":
        return _convert_temperature(value, from_unit, to_unit)

    units = CATEGORIES.get(category)
    if not units:
        raise ValueError(f"Unknown category: {category}")
    if from_unit not in units or to_unit not in units:
        raise ValueError("Unknown unit for this category.")

    base_value = value * units[from_unit]
    return base_value / units[to_unit]


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in TEMPERATURE_UNITS or to_unit not in TEMPERATURE_UNITS:
        raise ValueError("Unknown temperature unit.")

    if from_unit == to_unit:
        return value

    # Normalize to Celsius first.
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        raise ValueError("Unknown temperature unit.")

    if to_unit == "Celsius":
        return celsius
    if to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    if to_unit == "Kelvin":
        return celsius + 273.15
    raise ValueError("Unknown temperature unit.")
