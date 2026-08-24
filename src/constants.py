# src/constants.py

# -------------------------
# Window
# -------------------------
WINDOW_TITLE = "CalcSuite"
WINDOW_WIDTH = 460
WINDOW_HEIGHT = 760

# -------------------------
# Colors
# -------------------------
BACKGROUND_COLOR = "#1C1C1E"

NUMBER_BUTTON = "#2C2C2E"

OPERATOR_BUTTON = "#FF9F0A"

TEXT_COLOR = "#FFFFFF"

SECONDARY_TEXT = "#A1A1A6"

EQUALS_BUTTON = "#FF9F0A"

# -------------------------
# Fonts
# -------------------------

FONT_FAMILY = "Segoe UI"

EXPRESSION_FONT = (FONT_FAMILY, 18)

RESULT_FONT = (FONT_FAMILY, 60, "normal")

# -------------------------
# Padding
# -------------------------

WINDOW_PADDING = 20

DISPLAY_TOP_PADDING = 45

DISPLAY_BOTTOM_PADDING = 25

# -------------------------
# Display
# -------------------------

DISPLAY_HEIGHT = 250

# -------------------------
# Button Layout
# -------------------------

BUTTON_LAYOUT = [

    [
        {"text": "⌫", "type": "function"},
        {"text": "AC", "type": "function"},
        {"text": "%", "type": "function"},
        {"text": "÷", "type": "operator"},
    ],

    [
        {"text": "7", "type": "number"},
        {"text": "8", "type": "number"},
        {"text": "9", "type": "number"},
        {"text": "×", "type": "operator"},
    ],

    [
        {"text": "4", "type": "number"},
        {"text": "5", "type": "number"},
        {"text": "6", "type": "number"},
        {"text": "-", "type": "operator"},
    ],

    [
        {"text": "1", "type": "number"},
        {"text": "2", "type": "number"},
        {"text": "3", "type": "number"},
        {"text": "+", "type": "operator"},
    ],

    [
        {"text": "+/-", "type": "function"},
        {"text": "0", "type": "number"},
        {"text": ".", "type": "decimal"},
        {"text": "=", "type": "equals"},
    ]

]

# -------------------------
# Button Colors
# -------------------------

NUMBER_BUTTON = "#2C2C2E"

FUNCTION_BUTTON = "#5C5C5F"

OPERATOR_BUTTON = "#FF9F0A"

BUTTON_TEXT = "#FFFFFF"

# -------------------------
# Button Font
# -------------------------

BUTTON_FONT = (FONT_FAMILY, 18)