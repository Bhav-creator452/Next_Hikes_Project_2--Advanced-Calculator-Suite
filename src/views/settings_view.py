"""Settings view: theme, decimal precision, sound, history, shortcuts."""
import customtkinter as ctk

from src.components.dialogs import SectionHeader, Dropdown
from src.theme import theme_manager, FONTS

SHORTCUTS = [
    ("0-9", "Enter digits"),
    ("+ - * /", "Operators"),
    (".", "Decimal point"),
    ("Enter", "Equals"),
    ("Backspace", "Delete last entry"),
    ("Escape", "Clear (AC)"),
    ("%", "Percent"),
]


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, settings_manager, history_manager, on_theme_change=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)
        self.settings_manager = settings_manager
        self.history_manager = history_manager
        self.on_theme_change = on_theme_change

        self.grid_columnconfigure(0, weight=1)
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        scroll.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        SectionHeader(scroll, "Settings").grid(row=0, column=0, sticky="w", pady=(0, 16))

        self._row = 1
        self._build_theme_section(scroll)
        self._build_precision_section(scroll)
        self._build_sound_section(scroll)
        self._build_history_section(scroll)
        self._build_shortcuts_section(scroll)

    def _card(self, parent, title):
        colors = theme_manager.colors
        card = ctk.CTkFrame(parent, fg_color=colors.bg_secondary, corner_radius=14)
        card.grid(row=self._row, column=0, sticky="ew", pady=8)
        card.grid_columnconfigure(0, weight=1)
        self._row += 1
        ctk.CTkLabel(card, text=title, font=FONTS["body"], text_color=colors.text,
                     anchor="w").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))
        return card

    def _build_theme_section(self, parent):
        card = self._card(parent, "Theme")
        dropdown = Dropdown(card, values=["Dark", "Light", "System"], command=self._on_theme_change)
        dropdown.set(self.settings_manager.get("theme", "Dark"))
        dropdown.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

    def _on_theme_change(self, value):
        self.settings_manager.set("theme", value)
        if self.on_theme_change:
            self.on_theme_change(value)

    def _build_precision_section(self, parent):
        card = self._card(parent, "Decimal Places")
        dropdown = Dropdown(card, values=["Auto", "2", "4", "6", "8"], command=self._on_precision_change)
        dropdown.set(str(self.settings_manager.get("decimal_places", "Auto")))
        dropdown.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

    def _on_precision_change(self, value):
        self.settings_manager.set("decimal_places", value)

    def _build_sound_section(self, parent):
        card = self._card(parent, "Button Sound")
        colors = theme_manager.colors
        var = ctk.BooleanVar(value=self.settings_manager.get("sound_enabled", False))

        def _toggle():
            self.settings_manager.set("sound_enabled", var.get())

        switch = ctk.CTkSwitch(card, text="Play a sound on button press", variable=var,
                                command=_toggle, progress_color=colors.accent,
                                font=FONTS["label"], text_color=colors.text_secondary)
        switch.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

    def _build_history_section(self, parent):
        card = self._card(parent, "History")
        colors = theme_manager.colors
        var = ctk.BooleanVar(value=self.settings_manager.get("history_enabled", True))

        def _toggle():
            self.settings_manager.set("history_enabled", var.get())

        switch = ctk.CTkSwitch(card, text="Enable history recording", variable=var,
                                command=_toggle, progress_color=colors.accent,
                                font=FONTS["label"], text_color=colors.text_secondary)
        switch.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        clear_btn = ctk.CTkButton(card, text="Clear History", command=self._clear_history,
                                   fg_color=colors.error_bg, hover_color=colors.error_bg,
                                   text_color=colors.error, corner_radius=8, height=32)
        clear_btn.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 14))

    def _clear_history(self):
        self.history_manager.clear()

    def _build_shortcuts_section(self, parent):
        card = self._card(parent, "Keyboard Shortcuts")
        colors = theme_manager.colors
        row = 1
        for key, desc in SHORTCUTS:
            line = ctk.CTkFrame(card, fg_color="transparent")
            line.grid(row=row, column=0, sticky="ew", padx=16, pady=2)
            ctk.CTkLabel(line, text=key, font=FONTS["label"], text_color=colors.accent,
                         width=90, anchor="w").pack(side="left")
            ctk.CTkLabel(line, text=desc, font=FONTS["label"], text_color=colors.text_secondary,
                         anchor="w").pack(side="left")
            row += 1
        ctk.CTkLabel(card, text="", height=6).grid(row=row, column=0)
