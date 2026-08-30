"""
BMI calculation logic, independent of any UI framework.

Standard BMI thresholds (WHO):
    < 18.5       Underweight
    18.5 - 24.9  Normal
    25.0 - 29.9  Overweight
    >= 30.0      Obese
"""
from dataclasses import dataclass

CM_PER_INCH = 2.54
KG_PER_LB = 0.45359237


@dataclass(frozen=True)
class BMIResult:
    bmi: float
    category: str
    healthy_range_kg: tuple  # (min_kg, max_kg) for the person's height


def to_kg(weight: float, unit: str) -> float:
    if unit == "kg":
        return weight
    if unit == "lb":
        return weight * KG_PER_LB
    raise ValueError(f"Unsupported weight unit: {unit}")


def to_cm(height: float, unit: str, height_ft: float = 0, height_in: float = 0) -> float:
    if unit == "cm":
        return height
    if unit == "ft-in":
        total_inches = height_ft * 12 + height_in
        return total_inches * CM_PER_INCH
    raise ValueError(f"Unsupported height unit: {unit}")


def categorize(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_bmi(weight_kg: float, height_cm: float) -> BMIResult:
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Height and weight must be positive.")

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)

    min_healthy = round(18.5 * (height_m ** 2), 1)
    max_healthy = round(24.9 * (height_m ** 2), 1)

    return BMIResult(bmi=bmi, category=categorize(bmi), healthy_range_kg=(min_healthy, max_healthy))
