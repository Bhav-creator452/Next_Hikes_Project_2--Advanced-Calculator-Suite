"""
Centralized theme system for CalcSuite.

All modules must pull colors/fonts from here instead of hard-coding
values. This keeps the whole app visually consistent and makes
light/dark theming a one-place change.
"""
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Palette:
    bg: str
    bg_secondary: str
    bg_elevated: str
    text: str
    text_secondary: str
    text_muted: str
    button: str
    button_hover: str
    operator: str
    operator_hover: str
    accent: str
    accent_hover: str
    accent_text: str
    border: str
    error: str
    error_bg: str
    success: str
    success_bg: str
    sidebar_bg: str
    sidebar_active: str
    sidebar_hover: str


DARK = Palette(
    bg="#161616",
    bg_secondary="#1e1e1e",
    bg_elevated="#242424",
    text="#f5f5f5",
    text_secondary="#b5b5b5",
    text_muted="#7a7a7a",
    button="#2b2b2b",
    button_hover="#363636",
    operator="#ff9f2e",
    operator_hover="#ffb454",
    accent="#4f8cff",
    accent_hover="#6fa1ff",
    accent_text="#ffffff",
    border="#333333",
    error="#ff6b6b",
    error_bg="#3a1f1f",
    success="#57d68d",
    success_bg="#1f3a2a",
    sidebar_bg="#101010",
    sidebar_active="#2a2a2a",
    sidebar_hover="#1c1c1c",
)

LIGHT = Palette(
    bg="#f5f6f8",
    bg_secondary="#ffffff",
    bg_elevated="#ffffff",
    text="#1a1a1a",
    text_secondary="#4a4a4a",
    text_muted="#8a8a8a",
    button="#e9eaee",
    button_hover="#dcdde3",
    operator="#ff8a1e",
    operator_hover="#ff9f3f",
    accent="#3766e8",
    accent_hover="#5580f5",
    accent_text="#ffffff",
    border="#dcdde3",
    error="#d64545",
    error_bg="#fbe4e4",
    success="#2fa563",
    success_bg="#e3f6ea",
    sidebar_bg="#eceef2",
    sidebar_active="#ffffff",
    sidebar_hover="#e0e2e8",
)


FONT_FAMILY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"

FONTS: Dict[str, tuple] = {
    "display_result": (FONT_FAMILY, 44, "bold"),
    "display_result_small": (FONT_FAMILY, 30, "bold"),
    "display_expression": (FONT_FAMILY, 16, "normal"),
    "button": (FONT_FAMILY, 18, "normal"),
    "button_small": (FONT_FAMILY, 14, "normal"),
    "sidebar": (FONT_FAMILY, 14, "normal"),
    "sidebar_title": (FONT_FAMILY, 18, "bold"),
    "section_header": (FONT_FAMILY, 20, "bold"),
    "label": (FONT_FAMILY, 13, "normal"),
    "small": (FONT_FAMILY, 11, "normal"),
    "body": (FONT_FAMILY, 14, "normal"),
}

CORNER_RADIUS = 14
CORNER_RADIUS_SMALL = 8
BUTTON_SPACING = 8


class ThemeManager:
    """Runtime-swappable theme holder. Modules read `theme_manager.colors`."""

    def __init__(self, mode: str = "Dark"):
        self._mode = mode
        self.colors: Palette = DARK if mode == "Dark" else LIGHT

    def set_mode(self, mode: str) -> None:
        if mode not in ("Dark", "Light", "System"):
            mode = "Dark"
        if mode == "System":
            # No reliable cross-platform system-theme probe without extra
            # dependencies; default System to Dark.
            mode = "Dark"
        self._mode = mode
        self.colors = DARK if mode == "Dark" else LIGHT

    @property
    def mode(self) -> str:
        return self._mode


theme_manager = ThemeManager()
