"""Reusable button components shared across CalcSuite modules."""
import customtkinter as ctk

from src.theme import theme_manager, FONTS, CORNER_RADIUS_SMALL


class CalculatorButton(ctk.CTkButton):
    """
    A calculator keypad button with consistent sizing and a role-based
    color (number / operator / utility / equals) drawn from the theme.
    """

    ROLE_COLORS = {
        "number": lambda c: (c.button, c.button_hover, c.text),
        "operator": lambda c: (c.bg, c.button_hover, c.operator),
        "utility": lambda c: (c.bg_secondary, c.button_hover, c.text_secondary),
        "equals": lambda c: (c.accent, c.accent_hover, c.accent_text),
    }

    def __init__(self, master, text: str, command=None, role: str = "number",
                 font_key: str = "button", **kwargs):
        colors = theme_manager.colors
        fg, hover, text_color = self.ROLE_COLORS.get(role, self.ROLE_COLORS["number"])(colors)

        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=fg,
            hover_color=hover,
            text_color=text_color,
            corner_radius=CORNER_RADIUS_SMALL,
            font=FONTS.get(font_key, FONTS["button"]),
            border_width=0,
            **kwargs,
        )
        self.role = role

    def refresh_theme(self):
        colors = theme_manager.colors
        fg, hover, text_color = self.ROLE_COLORS.get(self.role, self.ROLE_COLORS["number"])(colors)
        self.configure(fg_color=fg, hover_color=hover, text_color=text_color)


class SwapButton(ctk.CTkButton):
    """Small round icon-style button used to swap From/To units or currencies."""

    def __init__(self, master, command=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(
            master,
            text="\u21c4",
            command=command,
            width=36,
            height=36,
            corner_radius=18,
            fg_color=colors.button,
            hover_color=colors.button_hover,
            text_color=colors.accent,
            font=FONTS["button_small"],
            **kwargs,
        )
