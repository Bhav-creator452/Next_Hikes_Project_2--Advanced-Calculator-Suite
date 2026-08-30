"""
Sidebar navigation.

Supports a collapsed (icon-only) mode for small windows, per the
responsive-layout requirement. The active module is visually
highlighted.
"""
import customtkinter as ctk

from src.theme import theme_manager, FONTS
from src.config import SIDEBAR_WIDTH_EXPANDED, SIDEBAR_WIDTH_COLLAPSED, APP_NAME

NAV_ITEMS = [
    ("standard", "\u25a3", "Standard"),
    ("scientific", "\u25a3", "Scientific"),
    ("bmi", "\u25a3", "BMI"),
    ("converter", "\u25a3", "Unit Converter"),
    ("currency", "\u25a3", "Currency"),
]

FOOTER_ITEMS = [
    ("history", "\u25a3", "History"),
    ("settings", "\u25a3", "Settings"),
    ("about", "\u25a3", "About"),
]


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_navigate, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.sidebar_bg, corner_radius=0,
                          width=SIDEBAR_WIDTH_EXPANDED, **kwargs)
        self.grid_propagate(False)

        self.on_navigate = on_navigate
        self.collapsed = False
        self.active_key = "standard"
        self._buttons = {}

        self._build()

    def _build(self):
        colors = theme_manager.colors

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(16, 8))

        self.title_label = ctk.CTkLabel(
            header, text=APP_NAME, font=FONTS["sidebar_title"], text_color=colors.text
        )
        self.title_label.pack(side="left")

        self.toggle_btn = ctk.CTkButton(
            header, text="\u2261", width=28, height=28, command=self.toggle_collapse,
            fg_color="transparent", hover_color=colors.sidebar_hover, text_color=colors.text_secondary,
        )
        self.toggle_btn.pack(side="right")

        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=8, pady=(8, 0))
        for key, icon, label in NAV_ITEMS:
            self._add_button(self.nav_frame, key, icon, label)

        sep = ctk.CTkFrame(self, fg_color=colors.border, height=1)
        sep.pack(fill="x", padx=12, pady=10)

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=8)
        for key, icon, label in FOOTER_ITEMS:
            self._add_button(self.footer_frame, key, icon, label)

        self.set_active("standard")

    def _add_button(self, parent, key, icon, label):
        colors = theme_manager.colors
        btn = ctk.CTkButton(
            parent, text=f"{icon}  {label}", anchor="w",
            fg_color="transparent", hover_color=colors.sidebar_hover,
            text_color=colors.text_secondary, font=FONTS["sidebar"],
            corner_radius=8, height=38,
            command=lambda k=key: self._handle_click(k),
        )
        btn.pack(fill="x", pady=2)
        self._buttons[key] = (btn, icon, label)

    def _handle_click(self, key):
        self.set_active(key)
        self.on_navigate(key)

    def set_active(self, key: str) -> None:
        colors = theme_manager.colors
        self.active_key = key
        for k, (btn, icon, label) in self._buttons.items():
            if k == key:
                btn.configure(fg_color=colors.sidebar_active, text_color=colors.text)
            else:
                btn.configure(fg_color="transparent", text_color=colors.text_secondary)

    def toggle_collapse(self) -> None:
        self.collapsed = not self.collapsed
        self.set_collapsed(self.collapsed)

    def set_collapsed(self, collapsed: bool) -> None:
        self.collapsed = collapsed
        width = SIDEBAR_WIDTH_COLLAPSED if collapsed else SIDEBAR_WIDTH_EXPANDED
        self.configure(width=width)
        self.title_label.pack_forget() if collapsed else None
        if not collapsed:
            self.title_label.pack(side="left")
        for key, (btn, icon, label) in self._buttons.items():
            btn.configure(text=icon if collapsed else f"{icon}  {label}")
