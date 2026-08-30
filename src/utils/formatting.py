"""
Number and result formatting helpers shared across all calculator modules.

Keeping this separate from calculation logic means the same clean
formatting rules apply to Standard, Scientific, BMI and Converter results.
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import math


def format_number(value, decimal_places="Auto", max_auto_places: int = 10) -> str:
    """
    Format a numeric value for display.

    - "Auto": trims trailing zeros / floating point noise (0.30000000000000004 -> 0.3)
    - "2"/"4"/"6"/"8": fixed decimal places
    - Uses thousands separators for large integers.
    - Falls back gracefully on inf/nan.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, float):
        if math.isnan(value):
            return "Undefined"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"

    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return str(value)

    if decimal_places != "Auto":
        try:
            places = int(decimal_places)
        except (TypeError, ValueError):
            places = max_auto_places
        quant = Decimal(1).scaleb(-places) if places > 0 else Decimal(1)
        try:
            dec = dec.quantize(quant, rounding=ROUND_HALF_UP)
        except InvalidOperation:
            pass
        text = format(dec, "f")
    else:
        # Auto: round to max_auto_places to kill float noise, then strip
        quant = Decimal(1).scaleb(-max_auto_places)
        try:
            dec = dec.quantize(quant, rounding=ROUND_HALF_UP)
        except InvalidOperation:
            pass
        text = format(dec.normalize(), "f")
        if text in ("", "-0"):
            text = "0"

    return _add_thousands_separators(text)


def _add_thousands_separators(text: str) -> str:
    negative = text.startswith("-")
    if negative:
        text = text[1:]

    if "." in text:
        int_part, frac_part = text.split(".", 1)
    else:
        int_part, frac_part = text, ""

    if len(int_part) > 3:
        rev = int_part[::-1]
        grouped = ",".join(rev[i:i + 3] for i in range(0, len(rev), 3))
        int_part = grouped[::-1]

    result = int_part + (("." + frac_part) if frac_part else "")
    return ("-" if negative else "") + result


def strip_grouping(text: str) -> str:
    """Remove thousands separators, e.g. for re-parsing display text."""
    return text.replace(",", "")


def safe_float(text) -> float:
    """Parse a possibly-grouped/blank numeric string into a float, defaulting to 0.0."""
    try:
        return float(strip_grouping(str(text)))
    except (TypeError, ValueError):
        return 0.0
