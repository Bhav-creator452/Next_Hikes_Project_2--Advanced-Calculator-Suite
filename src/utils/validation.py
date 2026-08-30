"""Shared validation helpers for form-style modules (BMI, Converter, Currency)."""


def is_blank(text) -> bool:
    return text is None or str(text).strip() == ""


def validate_positive_number(text, field_name="Value", min_value=0, max_value=None):
    """
    Validate that `text` is a real positive number.
    Returns (is_valid: bool, value_or_none: float|None, error_message: str|None)
    """
    if is_blank(text):
        return False, None, f"{field_name} is required."

    try:
        value = float(str(text).strip())
    except ValueError:
        return False, None, f"{field_name} must be a valid number."

    if value != value:  # NaN check
        return False, None, f"{field_name} must be a valid number."

    if value <= min_value:
        return False, None, f"{field_name} must be greater than {min_value}."

    if max_value is not None and value > max_value:
        return False, None, f"{field_name} seems unrealistic (max {max_value})."

    return True, value, None


def validate_bmi_inputs(height, weight, height_unit="cm", weight_unit="kg"):
    """Validate BMI form inputs with realistic ranges."""
    height_max = 300 if height_unit == "cm" else 10
    weight_max = 500 if weight_unit == "kg" else 1100

    ok_h, h_val, h_err = validate_positive_number(height, "Height", 0, height_max)
    if not ok_h:
        return False, None, None, h_err

    ok_w, w_val, w_err = validate_positive_number(weight, "Weight", 0, weight_max)
    if not ok_w:
        return False, None, None, w_err

    return True, h_val, w_val, None
