"""
CalcSuite main application.

Owns the window, sidebar, and module switching. Modules load inside
the same main window (no separate windows per calculator mode).
"""
import customtkinter as ctk

from src.config import (
    APP_NAME, DEFAULT_WINDOW_SIZE, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    SIDEBAR_COLLAPSE_BREAKPOINT,
)
from src.theme import theme_manager
from src.settings_manager import SettingsManager
from src.history_manager import HistoryManager

from src.components.sidebar import Sidebar

from src.modules.standard.ui import StandardCalculatorUI
from src.modules.scientific.ui import ScientificCalculatorUI
from src.modules.bmi.ui import BMICalculatorUI
from src.modules.converter.ui import UnitConverterUI
from src.modules.currency.ui import CurrencyConverterUI

from src.views.history_view import HistoryView
from src.views.settings_view import SettingsView
from src.views.about_view import AboutView


class CalcSuiteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Load configuration / settings / theme / history (startup order)
        self.settings_manager = SettingsManager()
        theme_manager.set_mode(self.settings_manager.get("theme", "Dark"))
        self.history_manager = HistoryManager()

        ctk.set_appearance_mode(theme_manager.mode)
        ctk.set_default_color_scheme = None  # we manage our own palette

        self.title(APP_NAME)
        self.geometry(DEFAULT_WINDOW_SIZE)
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.configure(fg_color=theme_manager.colors.bg)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, on_navigate=self.show_module)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self, fg_color=theme_manager.colors.bg, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._current_view = None
        self._module_builders = {
            "standard": self._build_standard,
            "scientific": self._build_scientific,
            "bmi": self._build_bmi,
            "converter": self._build_converter,
            "currency": self._build_currency,
            "history": self._build_history,
            "settings": self._build_settings,
            "about": self._build_about,
        }

        self.bind("<Configure>", self._on_resize)
        self._last_width = None

        self.show_module("standard")  # startup default

    # ---- module builders ------------------------------------------------
    def _build_standard(self):
        return StandardCalculatorUI(self.content, on_result=self._record_history("standard"))

    def _build_scientific(self):
        angle_mode = self.settings_manager.get("angle_mode", "DEG")
        return ScientificCalculatorUI(self.content, on_result=self._record_history("scientific"),
                                       angle_mode=angle_mode)

    def _build_bmi(self):
        return BMICalculatorUI(self.content, on_result=self._record_history("bmi"))

    def _build_converter(self):
        return UnitConverterUI(self.content, on_result=self._record_history("converter"))

    def _build_currency(self):
        return CurrencyConverterUI(self.content, on_result=self._record_history("currency"))

    def _build_history(self):
        return HistoryView(self.content, self.history_manager, on_reuse=self._on_history_reuse)

    def _build_settings(self):
        return SettingsView(self.content, self.settings_manager, self.history_manager,
                             on_theme_change=self._on_theme_change)

    def _build_about(self):
        return AboutView(self.content)

    # ---- navigation ---------------------------------------------------
    def show_module(self, key: str) -> None:
        if key not in self._module_builders:
            return
        if self._current_view is not None:
            self._current_view.destroy()

        self._current_view = self._module_builders[key]()
        self._current_view.grid(row=0, column=0, sticky="nsew")
        self.sidebar.set_active(key)
        self._current_key = key

    def _record_history(self, module: str):
        def _handler(expression: str, result: str):
            if self.settings_manager.get("history_enabled", True):
                self.history_manager.add_entry(module, expression, result)
        return _handler

    def _on_history_reuse(self, entry: dict):
        module = entry.get("module", "standard")
        expression = entry.get("expression", "")
        self.show_module(module if module in ("standard",) else "standard")
        if isinstance(self._current_view, StandardCalculatorUI):
            self._current_view.load_expression(expression)

    def _on_theme_change(self, mode: str) -> None:
        theme_manager.set_mode(mode)
        ctk.set_appearance_mode(theme_manager.mode)
        self.configure(fg_color=theme_manager.colors.bg)
        # Rebuild current view + sidebar so all colors refresh consistently.
        current_key = getattr(self, "_current_key", "standard")
        self.sidebar.destroy()
        self.sidebar = Sidebar(self, on_navigate=self.show_module)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.show_module(current_key)

    # ---- responsive behavior -------------------------------------------
    def _on_resize(self, event) -> None:
        if event.widget is not self:
            return
        width = event.width
        if width == self._last_width:
            return
        self._last_width = width
        should_collapse = width < SIDEBAR_COLLAPSE_BREAKPOINT
        if should_collapse != self.sidebar.collapsed:
            self.sidebar.set_collapsed(should_collapse)
