"""Unit Converter UI: conversion-focused layout."""
import customtkinter as ctk

from src.modules.converter.converter import get_categories, get_units, convert
from src.components.dialogs import SectionHeader, InputField, Dropdown
from src.components.buttons import SwapButton
from src.theme import theme_manager, FONTS
from src.utils.formatting import format_number, safe_float


class UnitConverterUI(ctk.CTkFrame):
    def __init__(self, master, on_result=None, **kwargs):
        colors = theme_manager.colors
        super().__init__(master, fg_color=colors.bg, **kwargs)
        self.on_result = on_result

        self.grid_columnconfigure(0, weight=1)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="n", pady=24)
        container.grid_columnconfigure(0, weight=1, minsize=420)

        SectionHeader(container, "Unit Converter").grid(row=0, column=0, sticky="w", padx=8, pady=(0, 16))

        card = ctk.CTkFrame(container, fg_color=colors.bg_secondary, corner_radius=14)
        card.grid(row=1, column=0, sticky="ew", padx=8)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(2, weight=1)

        categories = get_categories()
        self.category = Dropdown(card, values=categories, command=self._on_category_change)
        self.category.set(categories[0])
        self.category.grid(row=0, column=0, columnspan=3, sticky="ew", padx=16, pady=(16, 12))

        ctk.CTkLabel(card, text="From", font=FONTS["label"], text_color=colors.text_secondary,
                     anchor="w").grid(row=1, column=0, sticky="w", padx=16)
        ctk.CTkLabel(card, text="", width=36).grid(row=1, column=1)
        ctk.CTkLabel(card, text="To", font=FONTS["label"], text_color=colors.text_secondary,
                     anchor="w").grid(row=1, column=2, sticky="w", padx=16)

        self.from_unit = Dropdown(card, values=[], command=lambda v: self._recalculate())
        self.from_unit.grid(row=2, column=0, sticky="ew", padx=16)

        self.swap_btn = SwapButton(card, command=self._swap)
        self.swap_btn.grid(row=2, column=1, padx=4)

        self.to_unit = Dropdown(card, values=[], command=lambda v: self._recalculate())
        self.to_unit.grid(row=2, column=2, sticky="ew", padx=16)

        self.input_entry = InputField(card, placeholder="Enter value")
        self.input_entry.grid(row=3, column=0, columnspan=3, sticky="ew", padx=16, pady=(16, 8))
        self.input_entry.bind("<KeyRelease>", lambda e: self._recalculate())
        self.input_entry.insert(0, "1")

        self.result_label = ctk.CTkLabel(card, text="", font=FONTS["display_result_small"],
                                          text_color=colors.text, anchor="w")
        self.result_label.grid(row=4, column=0, columnspan=3, sticky="ew", padx=16, pady=(4, 20))

        # Populate initial units/result without recording a history entry —
        # history should only capture deliberate user input, not the
        # module's default startup state.
        self._suppress_history = True
        self._on_category_change(categories[0])
        self._suppress_history = False

    def _on_category_change(self, category: str):
        units = get_units(category)
        self.from_unit.configure(values=units)
        self.to_unit.configure(values=units)
        if units:
            self.from_unit.set(units[0])
            self.to_unit.set(units[1] if len(units) > 1 else units[0])
        self._recalculate()

    def _swap(self):
        f, t = self.from_unit.get(), self.to_unit.get()
        self.from_unit.set(t)
        self.to_unit.set(f)
        self._recalculate()

    def _recalculate(self):
        category = self.category.get()
        from_u = self.from_unit.get()
        to_u = self.to_unit.get()
        value = safe_float(self.input_entry.get())

        try:
            result = convert(category, value, from_u, to_u)
        except ValueError:
            self.result_label.configure(text="Invalid conversion")
            return

        formatted = format_number(result)
        self.result_label.configure(text=f"{formatted} {to_u}")

        if self.on_result and not self._suppress_history and self.input_entry.get().strip():
            expr = f"{format_number(value)} {from_u} \u2192 {to_u}"
            self.on_result(expr, formatted)
